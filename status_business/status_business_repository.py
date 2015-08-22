GET_TOTAL_CAPITAL_UP_DATE = "select sum(purchase_price) from tbl_order"
GET_TOTAL_ALL_ORDERS = "select sum(num_articles * unit_price) from tbl_order_details"
GET_TOTAL_PAYMENTS = "select sum(amount) from tbl_payment"
GET_DEBTORS = ("select tbl_order.id, customer, "
               "julianday('now')-julianday(date(tbl_order.date, 'unixepoch'))"
               "as order_date,"
               "julianday('now')-(select julianday(date(max(tbl_payment.date), "
               "'unixepoch')) "
               "from tbl_payment where order_id = tbl_order.id) as last_payment ,"
               "(select sum(tbl_payment.amount ) from tbl_payment "
               "where order_id = tbl_order.id) as total_payment,"
               "(select sum (num_articles * unit_price) from tbl_order_details "
               "where order_id = tbl_order.id) as total_order "
               "from tbl_order where total_payment is null or "
               "total_payment < total_order "
               "order by order_date desc, last_payment desc")


def get_total_capital_up_date(sql_connection):
    sql_cursor = sql_connection.cursor()
    sql_cursor.execute(GET_TOTAL_CAPITAL_UP_DATE)
    result = sql_cursor.fetchone()
    sql_cursor.close()
    return int(result[0])


def get_total_all_orders(sql_connection):
    sql_cursor = sql_connection.cursor()
    sql_cursor.execute(GET_TOTAL_ALL_ORDERS)
    result = sql_cursor.fetchone()
    sql_cursor.close()
    return int(result[0])


def get_total_payments(sql_connection):
    sql_cursor = sql_connection.cursor()
    sql_cursor.execute(GET_TOTAL_PAYMENTS)
    result = sql_cursor.fetchone()
    sql_cursor.close()
    return int(result[0])


def get_debtors(sql_connection):
    sql_cursor = sql_connection.cursor()
    sql_cursor.execute(GET_DEBTORS)
    results = sql_cursor.fetchall()
    sql_cursor.close()
    debtors = []
    for result in results:
        debtor = {
            "order_id": result[0],
            "customer": result[1],
            "order_days_ago": result[2],
            "last_payment_days_ago": result[3],
            "payment_up_date": result[4],
            "total_order": result[5]
        }
        debtors.append(debtor)
    return debtors
