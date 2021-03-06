from order import Order
from order_exceptions import OrderDetailsFoundException
from order_exceptions import OrderIdNotFoundException
from order_details import OrderDetails

INSERT_ORDER = ("insert into tbl_order "
                "('customer', 'date', 'customer_address', 'customer_phone',"
                " 'purchase_price', 'note') "
                "VALUES (?, ?, ?, ?, ?, ?)")


INSERT_ORDER_DETAILS = ("insert into tbl_order_details "
                        "('num_articles', 'description', 'unit_price', 'order_id') "
                        "VALUES (?, ?, ?, ?)")

GET_ORDERS_BY_CUSTOMER_NAME = ("select * from tbl_order "
                               "where customer like '%{customer}%'"
                               )

GET_ORDERS_BY_ORDER_ID = ("select * from tbl_order "
                          "where id = ?"
                          )


GET_ORDERS_DETAILS_BY_ORDER_ID = ("select * from tbl_order_details "
                                  "where order_id = ?"
                                  )


def save_order(sql_connection, order):
    sql_cursor = sql_connection.cursor()
    sql_cursor.execute('BEGIN TRANSACTION')
    sql_cursor.execute(INSERT_ORDER, (order.customer, order.date,
                                      order.customer_address,
                                      order.customer_phone,
                                      order.purchase_price,
                                      order.note))
    order_id = sql_cursor.lastrowid
    for order_detail in order.order_details:
        sql_cursor.execute(INSERT_ORDER_DETAILS, (order_detail.num_articles,
                           order_detail.description, order_detail.unit_price,
                           order_id))
    sql_cursor.close()
    sql_connection.commit()


def get_orders_by_customer_name(sql_connection, customer):
    sql_cursor = sql_connection.cursor()
    query = GET_ORDERS_BY_CUSTOMER_NAME.format(customer=customer)
    sql_cursor.execute(query)
    results = sql_cursor.fetchall()
    sql_cursor.close()
    orders = []
    for result in results:
        order = Order(result[0], result[1], result[2], result[3],
                      result[5], result[4], result[6], [])
        order.order_details = get_order_details_by_order_id(sql_connection, order.id)
        orders.append(order)

    return orders


def get_order_by_order_id(sql_connection, order_id):
    sql_cursor = sql_connection.cursor()
    sql_cursor.execute(GET_ORDERS_BY_ORDER_ID, (order_id,))
    result = sql_cursor.fetchone()
    sql_cursor.close()
    if result:
        order = Order(result[0], result[1], result[2], result[3],
                      result[5], result[4], result[6], [])
        order.order_details = get_order_details_by_order_id(sql_connection, order.id)
        return order
    raise OrderIdNotFoundException("order_id: %s, not found" % order_id)


def get_order_details_by_order_id(sql_connection, order_id):
    sql_cursor = sql_connection.cursor()
    sql_cursor.execute(GET_ORDERS_DETAILS_BY_ORDER_ID, (order_id,))
    results = sql_cursor.fetchall()
    sql_cursor.close()
    order_details = []
    if not results:
        raise OrderDetailsFoundException("order not found: %s" % order_id)

    for result in results:
        order_detail = OrderDetails(result[0], result[1], result[2], result[3], result[4])
        order_details.append(order_detail)
    return order_details

