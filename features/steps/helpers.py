from behave import *
from akulaku.akulaku import generate_signature, validate_response_signature


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
    context.signature = generate_signature(app_id=context.app_id, secret_key=context.secret, content=context.content)

@then("I expect the signature to be '{expected_signature}'")
def step_impl(context, expected_signature):
    assert context.signature == expected_signature


@given("a response from akulaku of {response_content}")
def step_impl(context, response_content):
    context.response = generate_signature(
        app_id=context.app_id,
        secret_key=context.secret,
        content=response_content
    )


@step("a valid signature signature")
def step_impl(context):
    context.expected_signature = context.response


@when("I validate the signature")
def step_impl(context):
    context.signature_valid = validate_response_signature(
        context.response,
        context.expected_signature
    )


@then("I expect True to be returned")
def step_impl(context):
    assert context.signature_valid is True
