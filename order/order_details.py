class OrderDetails:
    id = None,
    num_articles = None,
    description = None,
    unit_price = None,
    order_id = None

    def __init__(self, id, num_articles, description, unit_price, order_id):
        self.id = id
        self.num_articles = num_articles
        self.description = description
        self.unit_price = unit_price
        self.order_id = order_id




