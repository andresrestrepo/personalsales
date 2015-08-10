
INSERT_PAYMENT = ("insert into tbl_payment "
                  "('order_id', 'date', 'amount') "
                  "VALUES ({order_id}, {date}, {amount})")


def save_payment(sql_connection, payment):
    insert_payment = INSERT_PAYMENT.format(order_id=payment.order_id, date=payment.date,
                                           amount=payment.amount)
    sql_cursor = sql_connection.cursor()
    sql_cursor.execute(insert_payment)
    sql_connection.commit()
