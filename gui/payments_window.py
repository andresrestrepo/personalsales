import ScrolledText
import Tkinter
import time
import tkMessageBox
import sqlite3
import datetime
from config import dbconnection
from gui import query_order_window
from payment import payment_service, payment_repository
from payment.payment import Payment
from payment.payments_exceptions import PaymentExceedsValueDebtException, \
    InvalidAmountToSave


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
        payment = Payment(None, txt_order_id.get() or None, date or None,
                          txt_amount.get() or None)

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
        finally:
            sql_connection.close()

    def see_history():
        sql_connection = dbconnection.get_db_connection()
        payments = payment_repository.get_payments_by_order_id(sql_connection,
                                                               txt_order_id.get())
        txt_query.delete(1.0, Tkinter.END)
        for payment in payments:
            readable_date = datetime.datetime.fromtimestamp(int(payment.date)).\
                strftime('%Y-%m-%d')
            payment_str = "order:%s - date:%s - amount:%d" % \
                          (payment.order_id, readable_date, payment.amount)
            txt_query.insert(Tkinter.INSERT, payment_str)
            txt_query.insert(Tkinter.INSERT, "\n-------------------------------\n")

        txt_query.insert(Tkinter.INSERT, "****Total up date:%d" %
                         sum([payment.amount for payment in payments]))

        sql_connection.close()

    btn_save_payment = Tkinter.Button(root, text="Save", command=save_payment)
    btn_save_payment.place(x=20, y=130)

    btn_query_payments = Tkinter.Button(root, text="See History", command=see_history)
    btn_query_payments.place(x=100, y=130)

    txt_query = ScrolledText.ScrolledText(root, wrap=Tkinter.WORD, height=20, width=62)
    txt_query.place(x=20, y=180)

    root.mainloop()
