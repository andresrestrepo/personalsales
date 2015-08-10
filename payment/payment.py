class Payment:
    id = None
    order_id = None
    date = None
    amount = None

    def __init__(self, id, order_id, date, amount):
        self.id = id
        self.order_id = order_id
        self.date = date
        self.amount = amount
