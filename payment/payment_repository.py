from payment import Payment

INSERT_PAYMENT = ("insert into tbl_payment "
                  "('order_id', 'date', 'amount') "
                  "VALUES (?, ?, ?)")


GET_PAYMENTS_BY_ORDER_ID = ("select * from tbl_payment where order_id = ? "
                            "order by date desc")


def save_payment(sql_connection, payment):
    sql_cursor = sql_connection.cursor()
    sql_cursor.execute(INSERT_PAYMENT, (payment.order_id, payment.date, payment.amount))
    sql_cursor.close()
    sql_connection.commit()


def get_payments_by_order_id(sql_connection, order_id):
    sql_cursor = sql_connection.cursor()
    sql_cursor.execute(GET_PAYMENTS_BY_ORDER_ID, (order_id,))
    results = sql_cursor.fetchall()
    sql_cursor.close()
    payments = []
    for result in results:
        payment = Payment(result[0], result[1], result[2], result[3])
        payments.append(payment)

    return payments
