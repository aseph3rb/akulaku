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
        self.ref_number = ref_number,
        self.total_price = total_price,
        self.user_account = user_account,
        self.receiver_name = receiver_name
        self.receiver_phone = receiver_phone
        self.province = province
        self.city = city
        self.street = street
        self.postcode = postcode
        self.details = details if type(details) is str else details.serialize()

    def serialize(self):
        """

        :return:
        :rtype: dict
        """
        return {
            "refNo": self.ref_number,
            "totalPrice": self.total_price,
            "userAccount": self.user_account,
            "receiverName": self.receiver_name,
            "receiverPhone": self.receiver_phone,
            "province": self.province,
            "city": self.city,
            "street": self.street,
            "postcode": self.postcode,
            "details": self.details,
        }
