
INSERT_ORDER = ("insert into tbl_order "
                "('customer', 'date', 'customer_address', 'purchase_price') "
                "VALUES ('{customer}', {date}, '{customer_address}', {purchase_price})")


INSERT_ORDER_DETAILS = ("insert into tbl_order_details "
                        "('num_articles', 'description', 'unit_price', 'order_id') "
                        "VALUES ({num_articles}, '{description}', {unit_price}, {order_id})")


def save_order(sql_connection, order):
    insert_order = INSERT_ORDER.format(customer=order.customer, date=order.date,
                                       customer_address=order.customer_address,
                                       purchase_price=order.purchase_price)
    sql_cursor = sql_connection.cursor()
    sql_cursor.execute('BEGIN TRANSACTION')
    sql_cursor.execute(insert_order)
    for order_detail in order.order_details:
        insert_order_details = INSERT_ORDER_DETAILS.format(
            num_articles=order_detail.num_articles, description=order_detail.description,
            unit_price=order_detail.unit_price, order_id=sql_cursor.lastrowid
        )
        sql_cursor.execute(insert_order_details)
    sql_connection.commit()
