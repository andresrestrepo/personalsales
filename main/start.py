from config import dbconnection
from gui import order_window
from payment import payment_repository
from payment.payment import Payment


def _insert_payments():
    print "Insert payments"
    order_id = raw_input("Order Id:")
    date = raw_input("Date:")
    amount = raw_input("Amount:")
    payment = Payment(None, order_id, date, amount)
    sql_connection = dbconnection.get_db_connection()
    payment_repository.save_payment(sql_connection, payment)


if __name__ == "__main__":
    order_window.create_frame()



