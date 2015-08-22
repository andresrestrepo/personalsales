def get_total_order(order_details):
    total = [order_detail.num_articles * order_detail.unit_price
             for order_detail in order_details]
    return sum(total)
