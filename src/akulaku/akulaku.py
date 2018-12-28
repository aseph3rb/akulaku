import base64
import hashlib
import logging
# import requests
import json

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
        sign =generate_signature(app_id, secret_key, order_number)
        params = f'appId={self.app_id}&refNo={order_number}&sign={sign}&lang=id'
        return f'{self.base_url}/v2/openPay.html?{params}'

    def get_akulaku_response(self, order_number, user, shipping_address, basket):
        line = basket.lines.select_related('product').first()
        details = [{
            "skuId": line.product.stockrecords.first().partner_sku,
            "skuName": line.product.title,
            "unitPrice": int(line.unit_price_excl_tax),
            "qty": line.quantity,
        }]

        username = f'{user.first_name} {user.last_name}'
        street = shipping_address.line1 + shipping_address.line2 + shipping_address.line3 + shipping_address.line4
        total_price = int(line.unit_price_excl_tax * line.quantity)

        content = (f'{order_number}{total_price}{user.id}{username}{user.phone}{shipping_address.province.name}'
                   f'{shipping_address.regency_district.name}{street}{shipping_address.postcode}{details}')

        data = {
            "appId": self.app_id,
            "refNo": str(order_number),
            "totalPrice": str(total_price),
            "userAccount": str(user.id),
            "receiverName": username,
            "receiverPhone": user.phone,
            "province": shipping_address.province.name,
            "city": shipping_address.regency_district.name,
            "street": street,
            "postcode": shipping_address.postcode,
            "sign": self.get_sign(content),
            "details": str(details),
        }

        return self.generate_order(data, order_number)

    def generate_order(self, data, order_number):
        try:
            url = f'{self.base_url}/api/json/public/openpay/new.do'
            header = {
                'content-type': "multipart/form-data;",
                'Content-Type': "application/x-www-form-urlencoded"
            }

            response = requests.post(url, headers=header, data=data)

            json_response = response.json()
            if json_response["success"]:
                return json_response['data']['orderId']
            else:
                log.error(f"Failed to create new akulaku payment for order because data not valid")
                if json_response.get('errCode') == 'openpay.0002':
                    return json_response.get('errCode')

                raise UnableToTakePayment

        except Exception as e:
            log.exception(f"Failed to create new akulaku payment for order {order_number}")
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
