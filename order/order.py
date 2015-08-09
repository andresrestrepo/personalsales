class Order:
    id = None
    customer = None
    date = None
    customer_address = None
    purchase_price = None
    order_details = list()

    def __init__(self, id, customer, date, customer_addreess, purchase_price,
                 order_details):
        self.customer = customer
        self.id = id
        self.date = date
        self.customer_address = customer_addreess
        self.purchase_price = purchase_price
        self.order_details = order_details







