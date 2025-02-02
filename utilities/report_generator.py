"""
- does not have the charts

"""
import json
import argparse
import getpass as gp
import tzlocal as tzl
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument('--input_json_file',
                    required=True,
                    help="Path of input json file. JSON file is output of Behave test run")
parser.add_argument('--output_html_file',
                    required=True,
                    help="Path of the output html file to be generated")

args = parser.parse_args()

input_file = args.input_json_file
output_html_path = args.output_html_file


feature_count = 0
feature_failed_count = 0
feature_passed_count = 0
scenario_count = 0
scenario_failed_count = 0
scenario_passed_count = 0

all_rows = ""

feature_row_template = '''<p>Feature: {fe_name}</p>'''

scenario_row_template = '''<tr class="scenario">    
                                <td class="scenario_td">{sce_name}</td>
                                <td class="status" style="background: {scenario_status_background};">{sce_status}</td>
                            </tr>'''

step_row_template = '''<tr class="step" step_name="{step_name}" onClick="{on_click}">    
                                <td class="step_td">{step_name}</td>
                                <td class="status" style="color: {sc_status_color}; font-weight: {sc_status_font_weight}">{sce_status}</td>
                                <td class="screenshot">
                                <img src="/ReportingAndLogging/screenShots/TC1.png" width="320"height="180" onclick="window.open(this.src, '_blank');" ></img>
                                </td>
                            </tr>'''

error_row_template = '''<tr class="error_row" scenario_name="{sce_name}" style="background: #ffaaaa; display: none;">
                            <td class="err_sc_name scenario_td">{step_name}</td>
                            <td>{err}</td>
                        </tr>'''


report_styles = """
    <style>
        tr.scenario {
            background: #e1e3e1;
        }
        td.scenario_td {
            width:50%;
        }
        
        td.status {
            width: 10%;
            }
        
        td.err_sc_name {
            max-width: 100%;
        }
        td.feature_td {
            min-width:50;
        }
        table, th, td {
            border: 1px solid #1a7ade;
        }

    </style>

"""

report_javascript = """
    <script>
        function justalert(sc_name){
            var locator = 'tr.error_row[scenario_name="' + sc_name + '"]'
            var errRow = document.querySelector(locator)
            
            if ( errRow.style.display == "block") {
                errRow.style.display = "none";
            } else {
                errRow.style.display = "block";
            }
        }
    </script>
"""

# read the report json file
with open(input_file) as f:
    reports = json.load(f)


def calcuate_percent_passed():
    global scenario_failed_count
    global scenario_passed_count
    global scenario_count

    total_scenarios = scenario_failed_count + scenario_passed_count
    if total_scenarios != scenario_count:
        raise Exception("Number of total scenario count and failed + passed does not match.")
    try:
        pct_pass = round((scenario_passed_count/total_scenarios) * 100, 2)
    except ZeroDivisionError:
        pct_pass = 100

    return pct_pass

for report in reports:
    # verify each dictionary in the list is a feature
    _type = report['keyword']
    if _type == 'Feature':
        feature = report
    else:
        raise Exception("Unexpected top level keyword '{}'. Only expected 'Feature'".format(_type))

    # update the count of features passed/failed
    if feature['status'] == 'passed':
      feature_passed_count += 1
      feature_status_background = '#a5f1a5'
    elif feature['status'] == 'failed':
      feature_failed_count += 1
      feature_status_background = '#ffaaaa'

    else:
      raise Exception("Unexpected status for feature. Expected 'passed' or 'failed' but found '{}'".format(feature['status']))

    # add the feature as one row in the html table
    all_rows = all_rows + '''
<table>
    <thead></thead>
    <tbody>''' + feature_row_template.format(fe_name=feature['name'])
    feature_count += 1

    scenarios = feature['elements']
    for s in scenarios:
        s_type = s['type']
        if s_type == 'scenario':
            scenario = s
        else:
            raise Exception("Unexpected 'type' in list of elements for feature. Expected 'scenario' but found '{}'".format(s_type))

        scenario_name = scenario['name'].strip()
        if scenario['status'] == 'passed':
          scenario_passed_count += 1
          scenario_count += 1
          on_click = 'na'
          scenario_status_background = '#a5f1a5'
        elif scenario['status'] == 'failed':
          scenario_failed_count += 1
          scenario_count += 1
          on_click = "justalert('{}')".format(scenario_name)
          scenario_status_background = '#ffaaaa'

        else:
            raise Exception("Unexpected 'status' for scenario. Expected 'passed' or 'failed'. Actual: {}. Scenario name: {}".format(scenario['status'], scenario_name))

        # add the scenario row
        all_rows = all_rows + scenario_row_template.format(sce_name=scenario['name'], sce_status=scenario['status'].upper(),
                                                           scenario_status_background=scenario_status_background)

        ### Adding the step row
        for step in scenario['steps']:

            if len(step) == 6:
                if step['result']['status'] == 'passed':
                    sc_status_color = '#1c881c'
                    sc_status_font_weight = 'none'
                elif step['result']['status'] == 'failed':
                    sc_status_color = 'red'
                    sc_status_font_weight = 'bold'

                all_rows = all_rows + step_row_template.format(on_click=on_click,
                                                                   step_name=step['keyword'] + ' ' + step['name'],
                                                                   sce_status=step['result'].get('status').upper(),
                                                                   sc_status_color=sc_status_color,
                                                                   sc_status_font_weight=sc_status_font_weight)
        else:
            all_rows = all_rows + '</tbody>'


        # for the failed scenario the error needs to be added to the report so identify the step that failed and add the error
        if scenario['status'] == 'failed':
            steps = scenario['steps']

            for step in steps:
                try:
                    if step['result']['status'] == 'failed':
                        failed_step = step
                        break
                except:
                    pass
            else:
                raise Exception("There should be a failed step but none found in list of steps for scenario. Scenario name: {}".format(scenario_name))

            # add the error detail row
            all_rows = all_rows + error_row_template.format(
                sce_name=scenario_name,
                step_name=failed_step['keyword'] + ":" + failed_step['name'],
                err='<br>'.join(failed_step['result']['error_message']))



# Build the report summary
percent_passed = calcuate_percent_passed()

report_html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    {report_styles}
    <title>My Test Report</title>
</head>
<body>
<div id="test_summary">
         <h1> Test Report </h1>
         <p> Report generation date: {datetime.today().strftime("%Y %B %d at %I:%M:%S %p")} by Test Automation Framework
          </p>
         <h1> Environment </h1>
<table class="environment"> 
<tbody>
        <tr>
            <th>Tester</th>
            <td><center>Antonio Acosta Flores</center></td>
        </tr>
        <tr>
            <th>Story/Incident id</th>
            <td><center> - </center></td>
        </tr>
        <tr>
            <th>Environment</th>
            <td><center>SAT-SX-CG3</center></td>
        </tr>
        <tr>
            <th>Type of test</th>
            <td><center>Automated</center></td>
        </tr>
        <tr>
            <th>Test Automation Tool Name</th>
            <td><center>Automation Tests Framework</center></td>
        </tr>
        <tr>
            <th>Test execution date</th>
            <td><center>{datetime.today().strftime("%Y %B %d %a %I:%M:%S %p")}</center></td>
        </tr>
        <tr>
            <th>User name</th>
            <td><center>{gp.getuser()}</center></td>
        </tr>
        <tr>
            <th>Time zone</th>
            <td><center>{str(tzl.get_localzone())}</center></td>
        </tr>
</tbody>
</table>
         <h1> Summary </h1>
         <p> x tests took xtime </p>
         <h1> Execution Pass Rate: {percent_passed}% ({scenario_passed_count}/{(scenario_failed_count + scenario_passed_count)})</h1>
<table class="table-summary">
    <thead><th></th><th>PASSED</th><th>FAILED</th><th>PASS RATE</th></thead>
    <tbody>
        <tr>
            <th>Features</th><td style="color:green"><center>{feature_passed_count}</center></td>
            <td style="color:red"><center>{feature_failed_count}</center></td>
            <td><center>{round(feature_passed_count /(scenario_failed_count + feature_passed_count), 2) * 100} %</center></td>
        </tr>
        <tr>
            <th>Scenario</th><td style="color:green"><center>{scenario_passed_count}</center></td>
            <td style="color:red"><center>{scenario_failed_count}</center></td>
            <td><center>{round(scenario_passed_count/(scenario_failed_count + scenario_passed_count), 2) * 100} %</center></td>
        </tr>
    </tbody>
</table>
</div>
<h1>Execution details</h1>

{all_rows}

</table>
{report_javascript}
</body>
</html>"""



# reate the final report html
with open(output_html_path, 'w') as f:
    f.write(report_html_template)

print("***************************")
print("Feature count: {}".format(feature_count))
print("feature_failed_count: {}".format(feature_failed_count))
print("feature_passed_count: {}".format(feature_passed_count))
print("scenario_count: {}".format(scenario_count))
print("scenario_failed_count: {}".format(scenario_failed_count))
print("scenario_failed_count: {}".format(scenario_failed_count))
print("Output html: {}".format(output_html_path))
print("***************************")