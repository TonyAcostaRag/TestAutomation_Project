import subprocess


def run_tests(browser):

    feature_directory = 'tests/functional_tests/features'

    result = subprocess.run([
        'behave', '--format', 'html', '--outfile', 'reports/report.html',
        '--define', f'browser={browser}', feature_directory
    ])

    if result.returncode != 0:
        print(f"Tests failed on {browser}")
        return result.returncode
    else:
        print(f"Tests completed successfully on {browser}")
        return result.returncode


if __name__ == '__main__':

    browsers = ['chrome', 'firefox']
    for browser in browsers:
        run_tests(browser)
