Feature: verify the functionality of the login

  Scenario Outline: User can be redirected on home page due valid login
    Given User go to login page
    When User enter <username> and <password> credentials
    Then User is redirected to home page

    Examples:
    | username                | password     |
    | standard_user           | secret_sauce |
    | performance_glitch_user | secret_sauce |
    | problem_user            | secret_sauce |

  Scenario Outline: User is not authenticated due invalid credentials
    Given User go to login page
    When User enter <username> and <password> credentials
    Then Credentials do not match message is displayed in login page

    Examples:
    | username                | password             |
    | standard_user           | invalid_secret_sauce |
    | performance_glitch_user | invalid_secret_sauce |
    | problem_user            | invalid_secret_sauce |
    | non_existant_user       | secret_sauce         |

  Scenario Outline: User is not authenticated due is locked out
    Given User go to login page
    When User enter <username> and <password> credentials
    Then User locked out message is displayed in login page

    Examples:
    | username        | password     |
    | locked_out_user | secret_sauce |
