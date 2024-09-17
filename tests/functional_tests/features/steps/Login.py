from behave import given, when, then
from pages.Login import Login
from pages.Home import Home


@given(u'User go to login page')
def step_impl(context):
    context.login_page = Login(context.driver)
    context.login_page.go_to_page()


@when(u'User enter {username} and {password} credentials')
def step_impl(context, username, password):
    context.login_page.login(username, password)


@then(u'User is redirected to home page')
def step_impl(context):
    context.home_page = Home(context.driver)
    assert 'Products' in context.home_page.get_label_products()


@then(u'Credentials do not match message is displayed in login page')
def step_impl(context):
    assert 'Epic sadface:' in context.login_page.get_invalid_credentials_text()
    assert 'Username and password do not match any user in this service' in context.login_page.get_invalid_credentials_text()
    assert context.login_page.get_button_signin().is_displayed() is True


@then(u'User locked out message is displayed in login page')
def step_impl(context):
    assert 'Epic sadface:' in context.login_page.get_invalid_credentials_text()
    assert 'Sorry, this user has been locked out.' in context.login_page.get_invalid_credentials_text()
    assert context.login_page.get_button_signin().is_displayed() is True
