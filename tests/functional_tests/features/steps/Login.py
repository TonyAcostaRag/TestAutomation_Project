from behave import given, when, then
from pages.Login import Login
from pages.Home import Home


@given(u'User go to login page')
def step_impl(context):
    context.login_page = Login(context.driver)
    context.login_page.go_to_page()


@when(u'User enter valid {username} and {password} credentials')
def step_impl(context, username, password):
    context.login_page.login(username, password)


@then(u'User is redirected to home page')
def step_impl(context):
    context.home_page = Home(context.driver)
    assert 'Products' in context.home_page.get_label_products()
