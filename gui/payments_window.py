import ScrolledText
import Tkinter
import time
import tkMessageBox
import sqlite3
import datetime
from config import dbconnection
from gui import query_order_window
from order import order_repository, order_utils
from order.order_exceptions import OrderDetailsFoundException
from payment import payment_service, payment_repository
from payment.payment import Payment
from payment.payments_exceptions import PaymentExceedsValueDebtException, \
    InvalidAmountToSave
from status_business import status_business_service


def create_frame():
    root = Tkinter.Tk()
    root.eval('tk::PlaceWindow %s center' % root.winfo_pathname(root.winfo_id()))
    root.geometry('500x500')
    root.resizable(width=False, height=False)
    root.title("Payments")

    lbl_order_id = Tkinter.Label(root, text="Order Id: ")
    lbl_order_id.place(x=20, y=40)
    txt_order_id = Tkinter.Entry(root, width=30)
    txt_order_id.place(x=150, y=40)

    def query_order():
        query_order_window.create_frame()

    btn_query_order = Tkinter.Button(root, text="Search...", command=query_order)
    btn_query_order.place(x=400, y=40)

    lbl_date = Tkinter.Label(root, text="Date: ")
    lbl_date.place(x=20, y=70)
    txt_date = Tkinter.Entry(root, width=40)
    txt_date.place(x=150, y=70)
    txt_date.insert(0, str(time.strftime("%Y-%m-%d")))

    lbl_amount = Tkinter.Label(root, text="Amount: ")
    lbl_amount.place(x=20, y=100)
    txt_amount = Tkinter.Entry(root, width=40)
    txt_amount.place(x=150, y=100)

    def save_payment():
        date = int(datetime.datetime.strptime(txt_date.get(), '%Y-%m-%d').strftime("%s"))
        try:
            int_amount = int(txt_amount.get())
            payment = Payment(None, txt_order_id.get() or None, date or None,
                              int_amount or None)
        except ValueError as ex:
            tkMessageBox.showinfo("Error", ex.message)
            return

        sql_connection = dbconnection.get_db_connection()
        try:
            payment_service.save_payment(sql_connection, payment)
            tkMessageBox.showinfo("Message", "save data ok!")
        except PaymentExceedsValueDebtException as ex:
            tkMessageBox.showinfo("Error", ex.message)
        except InvalidAmountToSave as ex:
            tkMessageBox.showinfo("Error", ex.message)
        except sqlite3.IntegrityError, ex:
            tkMessageBox.showinfo("Error", ex.message)
        except OrderDetailsFoundException as ex:
            tkMessageBox.showinfo("Error", ex.message)
        finally:
            sql_connection.close()

    def see_history():
        sql_connection = dbconnection.get_db_connection()
        payments = payment_repository.get_payments_by_order_id(sql_connection,
                                                               txt_order_id.get())
        try:
            order_details = order_repository.get_order_details_by_order_id(
                sql_connection,
                txt_order_id.get())
        except OrderDetailsFoundException as ex:
            tkMessageBox.showinfo("Error", ex.message)
            return
        total_order = order_utils.get_total_order(order_details)
        txt_query.delete(1.0, Tkinter.END)
        count = 0
        for payment in payments:
            count += 1
            readable_date = datetime.datetime.fromtimestamp(int(payment.date)).\
                strftime('%Y-%m-%d')
            payment_str = "payment %d - date:%s - amount:%d" % \
                          (count, readable_date, payment.amount)
            txt_query.insert(Tkinter.INSERT, payment_str)
            txt_query.insert(Tkinter.INSERT, "\n-------------------------------\n")

        total_payments = sum([payment.amount for payment in payments])
        debt = total_order - total_payments
        txt_query.insert(Tkinter.INSERT, "****Total payments up date: %d \n" %
                         total_payments)
        txt_query.insert(Tkinter.INSERT, "****Total order price: %d \n" % total_order)
        txt_query.insert(Tkinter.INSERT, "****Debt up date: %d \n" % debt)
        if debt is 0:
            txt_query.insert(Tkinter.INSERT, "****Congratulations, order Ok! :)\n")

        sql_connection.close()

    def status_business():
        txt_query.delete(1.0, Tkinter.END)
        sql_connection = dbconnection.get_db_connection()
        total_capital_up_date = status_business_service.get_total_capital_up_date(
            sql_connection)
        total_orders = status_business_service.get_total_all_orders(sql_connection)
        total_debt = status_business_service.get_total_debt(sql_connection)
        total_balance = status_business_service.get_real_balance(sql_connection)
        profit = status_business_service.get_profit(sql_connection)
        txt_query.insert(Tkinter.INSERT, "****Total capital up date: %d \n" %
                         total_capital_up_date)
        txt_query.insert(Tkinter.INSERT, "****Total orders up date: %d \n" %
                         total_orders)
        txt_query.insert(Tkinter.INSERT, "****Total debt up date: %d \n" %
                         total_debt)
        if total_balance <= 0:
            txt_query.insert(Tkinter.INSERT, "****Total balance: %d, "
                                             "WARNING negative balance \n" %
                             total_balance)
        else:
            txt_query.insert(Tkinter.INSERT, "****Total balance: %d, "
                                             "CONGRATULATIONS balance is positive :) \n" %
                             total_balance)

        txt_query.insert(Tkinter.INSERT, "****Profit: %d, Estimate not real "
                                         "in money \n" % profit)

        txt_query.insert(Tkinter.INSERT, "\n***********DEBTORS***********\n\n")
        debtors = status_business_service.get_debtors(sql_connection)
        _paint_debtors(debtors)
        sql_connection.close()

    def _paint_debtors(debtors):
        for debtor in debtors:
            txt_query.insert(Tkinter.INSERT, "order: %s \n" % debtor["order_id"])
            txt_query.insert(Tkinter.INSERT, "customer: %s \n" % debtor["customer"])
            txt_query.insert(Tkinter.INSERT, "order created %s days ago \n" %
                             int(debtor["order_days_ago"]))

            if debtor["last_payment_days_ago"]:
                if int(debtor["last_payment_days_ago"]) == 0:
                    txt_query.insert(Tkinter.INSERT, "last payment today \n")
                else:
                    txt_query.insert(Tkinter.INSERT, "last payment %s days ago \n" %
                                     int(debtor["last_payment_days_ago"]))
            else:
                txt_query.insert(Tkinter.INSERT, "last payment: Never! \n")

            debt = debtor["total_order"]
            if debtor["payment_up_date"]:
                txt_query.insert(Tkinter.INSERT, "payments up date: %d \n" %
                                 debtor["payment_up_date"])
                debt = int(debtor["total_order"]) - int(debtor["payment_up_date"])
            else:
                txt_query.insert(Tkinter.INSERT, "payments up date: 0 \n")

            txt_query.insert(Tkinter.INSERT, "total order: %d \n" % debtor["total_order"])
            txt_query.insert(Tkinter.INSERT, "debt: %d \n" % debt)

            txt_query.insert(Tkinter.INSERT, "\n-----------------//-------------------\n")

    btn_save_payment = Tkinter.Button(root, text="Save", command=save_payment)
    btn_save_payment.place(x=20, y=130)

    btn_query_payments = Tkinter.Button(root, text="See History", command=see_history)
    btn_query_payments.place(x=100, y=130)

    btn_status_business = Tkinter.Button(root, text="Status Business",
                                         command=status_business)
    btn_status_business.place(x=200, y=130)

    txt_query = ScrolledText.ScrolledText(root, wrap=Tkinter.WORD, height=20, width=62)
    txt_query.place(x=20, y=180)

    root.mainloop()
