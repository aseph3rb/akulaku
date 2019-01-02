import base64
import hashlib
import logging
import requests
import json

from akulaku.exceptions import AkulakuError
from .akulaku_helpers import on_payment_updated

log = logging.getLogger('akulaku')


def validate_response_signature(expected_signature, response_signature):
    """ to validate response signature
    :param 'str' expected_signature:
    :param 'str' response_content:
    :return: bool
    """
    return expected_signature == response_signature


def generate_signature(app_id, secret_key, content):
    """ Create a signature for an Akulaku api request

    :param `str` app_id: A unique app ID given by Akulaku
    :param `str` secret_key: A unique secret key given by Akulaku
    :param `str` content: The stringified content of the request.
    :return: str
    """
    content = f'{app_id}{secret_key}{content}'
    has_sha512 = hashlib.sha512(content.encode()).digest()
    encoded = base64.b64encode(has_sha512)

    encoded_string = encoded.decode('utf-8')
    return encoded_string.replace("+", "-").replace("/", "_").replace("=", "")


class AkulakuGateway:

    def __init__(self, app_id, secret_key, use_sandbox=False):
        self.app_id = app_id
        self.secret_key = secret_key
        self.use_sandbox = use_sandbox

    @property
    def base_url(self):
        return "http://testmall.akulaku.com" if self.use_sandbox \
            else "https://mall.akulaku.com"

    def get_url_akulaku(self, app_id, secret_key, order_number):
        sign = generate_signature(app_id, secret_key, order_number)
        params = f'appId={self.app_id}&refNo={order_number}&sign={sign}&lang=id'
        return f'{self.base_url}/v2/openPay.html?{params}'

    def generate_new_order_akulaku(self, order_request):
        """

        :param `akulaku.akulaku_models.NewOrderRequest` order_request:
        :return:
        :rtype: int
        """
        data = order_request.serialize()
        content = (f'{order_request.ref_number}{order_request.ref_number}{order_request.user_account}'
                   f'{order_request.receiver_name}{order_request.receiver_phone}{order_request.province}'
                   f'{order_request.city}{order_request.street}{order_request.postcode}{order_request.details}')

        data.update({
            "appId": self.app_id,
            "sign": generate_signature(self.app_id, self.secret_key, content)
        })

        try:
            url = f'{self.base_url}/api/json/public/openpay/new.do'
            header = {
                'Content-Type': "application/x-www-form-urlencoded"
            }

            response = requests.post(url, headers=header, data=data)

            json_response = response.json()
            if json_response["success"]:
                return json_response['data']['orderId']
            else:
                raise AkulakuError(f'AkuLaku return an error: code={json_response.get("errCode")}')

        except Exception:
            log.exception(f"Failed to create new akulaku payment for order {order_request.ref_number}")
            raise

    def get_order(self, order_number):
        try:
            url = f'{self.base_url}/api/json/public/openpay/status.do'
            params = {
                "appId": self.app_id,
                "refNo": str(order_number),
                "sign": self.get_sign(str(order_number))
            }

            response = requests.get(url=url, params=params)
            json_response = response.json()

            if json_response["success"]:
                return json_response['data']
            else:
                log.error(f"Failed to create new akulaku payment for order because data not valid")

        except Exception as e:
            log.exception(f"Failed to create new akulaku payment for order {order_number}")
            raise e
