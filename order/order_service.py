import order_repository, order_utils
from order_exceptions import OrderDetailsEmptyException, \
    PurchasePriceBiggerTotalOrderException


def save_order(sql_connection, order):
    _validate_order_before_save(order)
    order_repository.save_order(sql_connection, order)


def _validate_order_before_save(order):
    if len(order.order_details) == 0:
        raise OrderDetailsEmptyException("Details can't be empty")
    total_details = order_utils.get_total_order(order.order_details)
    if order.purchase_price >= total_details:
        raise PurchasePriceBiggerTotalOrderException(
            "purchase price cant be equal or bigger than total order")


