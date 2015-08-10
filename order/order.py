class Order:
    id = None
    customer = None
    date = None
    customer_address = None
    customer_phone = None
    purchase_price = None
    note = None
    order_details = list()

    def __init__(self, id, customer, date, customer_addreess, customer_phone,
                 purchase_price, note,
                 order_details):
        self.customer = customer
        self.id = id
        self.date = date
        self.customer_address = customer_addreess
        self.customer_phone = customer_phone
        self.purchase_price = purchase_price
        self.note = note
        self.order_details = order_details







