from http import HTTPStatus
from unittest.mock import patch, MagicMock

from behave import *
from requests import Response

from akulaku.akulaku import AkulakuGateway
from akulaku.akulaku_models import NewOrderRequest, OrderDetail
from akulaku.exceptions import AkulakuError


@given("a gateway with app id of {app_id}, secret key of {secret_key}, sandbox is {sandbox}")
def step_impl(context, app_id, secret_key, sandbox):
    context.gateway = AkulakuGateway(
        app_id=app_id,
        secret_key=secret_key,
        use_sandbox=(True if sandbox == "True" else False)
    )


@when("i check base url")
def step_impl(context):
    context.base_url = context.gateway.base_url

@then('i get url "{url}"')
def step_impl(context, url):
    assert context.base_url == url


@when("i try to get akulaku url")
def step_impl(context):
    context.akulaku_url = context.gateway.get_url_akulaku(
        context.gateway.app_id, context.gateway.secret_key, context.order_number)


@then('i get akulaku url "{url}"')
def step_impl(context, url):
    assert context.akulaku_url == url


@step("order number of {order_number}")
def step_impl(context, order_number):
    context.order_number = order_number


@given("object OrderRequest")
def step_impl(context):
    context.order_request = NewOrderRequest(
        ref_number='1001',
        total_price='600000',
        user_account='1',
        receiver_name='fuad',
        receiver_phone='085778869436',
        province='Jawa Barat',
        city='Kab. Bekasi',
        street='Jln Srigunting 3',
        postcode='17325',
        details=OrderDetail(
            sku='1001',
            name='My Great Product',
            unit_price=100000,
            quantity=6
        )
    )


@when("I make a successful new order request")
def step_impl(context):

    mock_post = MagicMock(spec=Response)
    mock_post.status_code = HTTPStatus.OK
    mock_post.json.return_value = {
        "success": True,
        "sysTime": 1545384269735,
        "data": {
            "orderId": 78681
        },
        "errCode": "",
        "errMsg": ""
    }

    patcher = patch('akulaku.akulaku.requests')
    fake_requests = patcher.start()
    fake_requests.post.return_value = mock_post

    context.response_order_id = context.gateway.generate_new_order_akulaku(
        context.order_request
    )

    patcher.stop()


@then("i get orderId response")
def step_impl(context):
    assert context.response_order_id == 78681


@when("I make a error response")
def step_impl(context):

    mock_post = MagicMock(spec=Response)
    mock_post.status_code =HTTPStatus.OK
    mock_post.json.return_value = {
        "success": False,
        "sysTime": 1546420589044,
        "errCode": "openpay.0001",
        "errMsg": "invalid sign, content=12345608123123123fuad pratama085778869436Jawa BaratKab. BekasiJln.Sriguntung No. 317325[{\"skuId\":\"10013\",\"skuName\":\"IOS123\",\"unitPrice\":1000000,\"qty\": 1,\"img\": \"https://ecs7.tokopedia.net/img/cache/700/product-1/2017/12/25/0/0_d67d57ce-ca4d-48f7-ad2d-623fc1f7f43e_512_512.jpg\", \"vendorName\":\"iphone store\", \"vendorId\":\"ipone0001\"}],sign=aouQppCP3_ir4UwwXuYGfpsLUJ4CizXMKxbz1MvR4MQFFTUj7XDqyx8qs39h3kFKkOjY38auk4e3trKBX71W3wdff,correctSign=aouQppCP3_ir4UwwXuYGfpsLUJ4CizXMKxbz1MvR4MQFFTUj7XDqyx8qs39h3kFKkOjY38auk4e3trKBX71W3w",
    }

    patcher = patch('akulaku.akulaku.requests')
    fake_requests = patcher.start()
    fake_requests.post.return_value = mock_post

    try:
        context.response_error = context.gateway.generate_new_order_akulaku(
            context.order_request
        )
    except Exception as e:
        context.response_error = e

    patcher.stop()


@then("i get Akulaku Error")
def step_impl(context):
    assert context.response_error == AkulakuError(f'AkuLaku return an error: code=openpay.0001')
