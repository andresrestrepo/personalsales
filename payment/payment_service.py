from order import order_repository, order_utils
import payment_repository
from payments_exceptions import PaymentExceedsValueDebtException, InvalidAmountToSave


def save_payment(sql_connection, payment):
    _validate_payment_before_save(sql_connection, payment)
    payment_repository.save_payment(sql_connection, payment)


def _validate_payment_before_save(sql_connection, payment):
    order_details = order_repository.get_order_details_by_order_id(sql_connection,
                                                                   payment.order_id)
    payments = payment_repository.get_payments_by_order_id(sql_connection,
                                                           payment.order_id)
    total_order = order_utils.get_total_order(order_details)
    total_payments = _get_total_payments_up_date(payments)
    if payment.amount + total_payments > total_order:
        debt = total_order - total_payments
        raise PaymentExceedsValueDebtException("please check the amount, the debt is:%d"
                                               % debt)
    if payment.amount <= 0:
        raise InvalidAmountToSave("Amount needs to be bigger than 0")


def _get_total_payments_up_date(payments):
    total = [payment.amount for payment in payments]
    return sum(total)
