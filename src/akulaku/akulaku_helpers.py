import http
import logging

# from django.http import JsonResponse
# from oscar.core.loading import get_model
#
# from apps.payment.models import PAID, CANCELED
# from apps.payment.akulaku_models import AK_PENDING, AK_FAILED, AK_CANCELLLED, \
#     AK_SUCCESS, AkuLakuStatus
#
# from .akulaku import AkulakuPayment
# from apps.order.models import PaymentEvent, PaymentEventQuantity, PaymentEventType
#
# Source = get_model('payment', 'Source')
# PaymentTransaction = get_model('payment', 'Transaction')

log = logging.getLogger('simpati')


def on_payment_updated(order, response):
    order = order
    status = response.get('status')

    if status == AkuLakuStatus.PENDING:
        return process_placed_order(order, response)
    elif status == AK_FAILED:
        return process_expired_order(order, response)
    elif status == AK_CANCELLLED:
        return                                          # BELUM ADA
    elif status == AK_SUCCESS:
        return process_paid_order(order, response)


def create_payment_transaction(order, source, order_exist):
    log.info(f'[order]: {order} , [source]: {source} , [order_exist]: {order_exist}')

    transaction = PaymentTransaction.objects.create(source=source, amount=order.total_incl_tax)
    transaction.txn_type = 'akulaku'
    transaction.reference = source.reference
    if (order.status != PAID) and (order_exist.get('status') == AK_SUCCESS):
        transaction.status = PAID
    else:
        transaction.status = order_exist.get('status')  # HARUS DIGANTI
    transaction.save()
    return transaction


def create_order_event(order, expired=False):
    event_type, __ = PaymentEventType.objects.get_or_create(
        name='akulaku')

    event = PaymentEvent.objects.create(
        order=order,
        event_type=event_type, amount=order.total_incl_tax,
        reference='akulaku')

    for line in order.lines.all():
        PaymentEventQuantity.objects.create(
            event=event, line=line, quantity=line.quantity)

        if expired:
            line.stockrecord.cancel_allocation(line.quantity)
    log.info(f"finish create order event for {order}")


def create_order_notes(order, order_exist, expired=False):
    status = CANCELED if expired else order_exist.get('status')  # PERLU DIUBAH
    order.notes.create(
        message=f"order number: {order_exist.get('refNo')} , status: {status}",
        note_type="System", user=order.user
    )


def process_placed_order(order, **kwargs):
    """

    :param order: Order object
    :param kwargs:
    :return:
    """
    source = Source.objects.get(order=order)
    akulaku_payment = AkulakuPayment()
    order_exist = akulaku_payment.get_order(kwargs.get('refNo'))

    create_payment_transaction(order, source, order_exist)
    create_order_event(order)
    create_order_notes(order, order_exist)

    log.info(f"Order Id {order.number} has been Placed by : System")
    return JsonResponse({"message": "Success"}, status=http.HTTPStatus.OK)


def process_paid_order(order, **kwargs):
    """ Explain what you're doing here.

    :param `apps.orders.models.Order` order: DESCRIBE SOMETHING HERE
    :param `dict` kwargs:
    :return: django.http.JsonResponse
    """

    source = Source.objects.get(order=order)
    akulaku_payment = AkulakuPayment()
    order_exist = akulaku_payment.get_order(kwargs.get('refNo'))

    if (order.status == PAID) and (order_exist.get('status') == AK_SUCCESS):
        return JsonResponse({"message": "Already Paid"}, status=http.HTTPStatus.OK)

    create_payment_transaction(order, source, order_exist)
    order.set_status(PAID)
    source.amount_debited = order.total_incl_tax
    source.save()

    create_order_event(order)
    create_order_notes(order, order_exist)

    # send_email_paid(order, request=kwargs.get("request"))

    log.info(f"Order Id {order.number} has been Paid")
    return JsonResponse({"message": "Success"}, status=http.HTTPStatus.OK)


def process_expired_order(order, **kwargs):
    """

    :param order: Order object
    :param kwargs:
    :return:
    """
    order.set_status(CANCELED)
    source = Source.objects.get(order=order)
    akulaku_payment = AkulakuPayment()
    order_exist = akulaku_payment.get_order(kwargs.get('refNo'))

    create_payment_transaction(order, source, order_exist)
    create_order_event(order, expired=True)
    create_order_notes(order, order_exist, expired=True)

    log.info(f"Order Id {order.number} has been Cancelled by : System")

    return JsonResponse({"message": "Success"}, status=http.HTTPStatus.OK)


# def process_cancel_order( request, order=False):
#     client = ApiClient(settings.MIDTRANS.get("SERVER_KEY"), settings.MIDTRANS.get("SANDBOX"))
#     order_id = order if order else QueryDict(request.body).get("order")
#     response = client.cancel_payment(order_id)
#     log.info(f"Order Id {order_id} has been Cancelled by : {request.user}")
#     return response
