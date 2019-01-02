from behave import *

from akulaku.akulaku_models import NewOrderRequest, OrderDetail


@given("a create order request")
def step_impl(context):
    context.entity = NewOrderRequest(
        ref_number='1001',
        total_price='2000000',
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
        ).serialize()
    )

@then("the order request is converted to a dictionary properly")
def step_impl(context):
    assert context.serialized == {
            "refNo": context.entity.ref_number,
            "totalPrice": total_price,
            "userAccount": user_account,
            "receiverName": receiver_name,
            "receiverPhone": receiver_phone,
            "province": province,
            "city": city,
            "street": street,
            "postcode": postcode,
            "details": details
    }

@given("an OrderDetail with sku = {sku}, name = {name}, unit_price = {unit_price}, quantity = {quantity}")
def step_impl(context, sku, name, unit_price, quantity):
    context.entity = OrderDetail(
        sku=sku,
        name=name,
        unit_price=unit_price,
        quantity=quantity
    )

@when("I serialize the object")
def step_impl(context):
    context.serialized = context.entity.serialize()


@then("the OrderDetail is serialized correctly")
def step_impl(context):
    assert context.serialized == (
        f'[{{"skuId": "{context.entity.sku}", ' 
        f'"skuName": "{context.entity.name}", '
        f'"unitPrice": {context.entity.unit_price}, '
        f'"qty": {context.entity.quantity}}}]'
    ), f'context.serialized was {context.serialized}'
