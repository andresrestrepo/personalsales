class OrderIdNotFoundException(Exception):
    pass


class OrderDetailsEmptyException(Exception):
    pass


class PurchasePriceBiggerTotalOrderException(Exception):
    pass


class OrderDetailsFoundException(Exception):
    pass
