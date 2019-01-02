from enum import IntEnum


class AkuLakuStatus(IntEnum):
    PENDING = 1
    REFUND = 91
    FAILED = 90
    CANCELLED = 92
    SUCCESS = 100
    RECEIPTED = 101


class OrderDetail:
    def __init__(self,
                sku,
                name,
                unit_price,
                quantity):
        self.sku = sku
        self.name = name
        self.unit_price = unit_price
        self.quantity = quantity

    def serialize(self):
        return (f'[{{"skuId": "{self.sku}", '
                f'"skuName": "{self.name}", '
                f'"unitPrice": {self.unit_price}, '
                f'"qty": {self.quantity}}}]')

class NewOrderRequest:
    def __init__(self,
                 ref_number,
                 total_price,
                 user_account,
                 receiver_name,
                 receiver_phone,
                 province,
                 city,
                 street,
                 postcode,
                 details
                 ):
            pass

    def serizalize(self):
        # return {
        #     "appId": app_id,
        #     "refNo": ref_number,
        #     "totalPrice": total_price,
        #     "userAccount": user_account,
        #     "receiverName": receiver_name,
        #     "receiverPhone": receiver_phone,
        #     "province": province,
        #     "city": city,
        #     "street": street,
        #     "postcode": postcode,
        #     "sign": signature,
        #     "details": details,
        # }
