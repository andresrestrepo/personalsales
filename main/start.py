from config import dbconnection
from order import order_repository
from order.order import Order
from order.order_details import OrderDetails


def _main():
    print "Menu"
    print "1-> Save order"
    print "2-> Query order"
    option = raw_input("Select one option:")
    options = {'1': _save_order,
               '2': _query_order
               }
    options[option]()


def _save_order():
    print "save order"
    customer = raw_input("Customer Name:")
    date = raw_input("Date:")
    customer_address = raw_input("Customer Address:")
    purchase_price = raw_input("Purchase Price:")
    order = Order(None, customer, date, customer_address, purchase_price, list())
    while True:
        print "save order details"
        num_articles = raw_input("Num Articles:")
        description = raw_input("Article Description:")
        unit_price = raw_input("Unit Price:")
        order_details = OrderDetails(None, num_articles, description, unit_price, None)
        order.order_details.append(order_details)

        option_more_details = raw_input("Insert Other detail?:")
        if option_more_details.lower() == 'n':
            break

    sql_connection = dbconnection.get_db_connection()
    order_repository.save_order(sql_connection, order)


def _query_order():
    print "query order"
    pass


if __name__ == "__main__":
    _main()
