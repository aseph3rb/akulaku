from behave import *
from akulaku.akulaku import get_sign


@step('I have this content {content_value}')
def step_impl(context, content_value):
    context.content = content_value


@given("I have an app_id of {app_id}")
def step_impl(context, app_id):
    context.app_id = 123


@step("I have a secret of {secret}")
def step_impl(context, secret):
    context.secret = secret

@when("I generate a signature")
def step_impl(context):
    context.signature = get_sign(
        app_id=context.app_id,
        secret_key=context.secret,
        content=context.content
    )

@then("I expect the signature to be '{expected_signature}'")
def step_impl(context, expected_signature):
    assert context.signature == expected_signature
