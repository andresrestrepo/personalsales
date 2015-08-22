from status_business import status_business_repository


def get_total_capital_up_date(sql_connection):
    return status_business_repository.get_total_capital_up_date(sql_connection)


def get_total_all_orders(sql_connection):
    return status_business_repository.get_total_all_orders(sql_connection)


def get_total_debt(sql_connection):
    total_orders = status_business_repository.get_total_all_orders(sql_connection)
    total_payments = status_business_repository.get_total_payments(sql_connection)
    return total_orders - total_payments


def get_real_balance(sql_connection):
    total_capital = status_business_repository.get_total_capital_up_date(sql_connection)
    total_payments = status_business_repository.get_total_payments(sql_connection)
    return total_payments - total_capital


def get_profit(sql_connection):
    total_orders = status_business_repository.get_total_all_orders(sql_connection)
    total_capital = status_business_repository.get_total_capital_up_date(sql_connection)
    return total_orders - total_capital


def get_debtors(sql_connection):
    return status_business_repository.get_debtors(sql_connection)

