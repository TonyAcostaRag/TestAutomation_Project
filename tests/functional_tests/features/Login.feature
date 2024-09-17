Feature: verify the functionality of the login

  Scenario Outline: Valid login into page
    Given User go to login page
    When User enter valid <username> and <password> credentials
    Then User is redirected to home page

    Examples:
    | username      | password     |
    | standard_user | secret_sauce |
