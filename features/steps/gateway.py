from behave import *
from akulaku.akulaku import AkulakuGateway


@given("a gateway with app id of {app_id}, secret key of {secret_key}, sandbox is {sandbox}")
def step_impl(context, app_id, secret_key, sandbox):
    context.app_id = app_id
    context.secret_key = secret_key

    sandbox = True if sandbox == "True" else False
    context.sandbox = sandbox


@when("i check base url")
def step_impl(context):
    context.akulaku = AkulakuGateway(context.app_id, context.secret_key, use_sandbox=context.sandbox)


@then('i get url "{url}"')
def step_impl(context, url):
    assert context.akulaku.base_url == url


@when("i try to get akulaku url")
def step_impl(context):
    akulaku = AkulakuGateway(context.app_id, context.secret_key, use_sandbox=context.sandbox)
    context.akulaku_url = akulaku.get_url_akulaku(context.app_id, context.secret_key, context.order_number)


@then('i get akulaku url "{url}"')
def step_impl(context, url):
    assert context.akulaku_url == url


@step("order number of {order_number}")
def step_impl(context, order_number):
    context.order_number = order_number
