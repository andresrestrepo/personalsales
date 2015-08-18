import ScrolledText
import Tkinter
import time
import tkMessageBox
import datetime
from config import dbconnection
from gui import query_order_window, payments_window
from order import order_repository
from order.order import Order
from order.order_details import OrderDetails


def _save_order(customer, date, customer_address, customer_phone, purchase_price,
                note, order_details):
    order = Order(None, customer, date, customer_address,
                  customer_phone, purchase_price, note, list())

    for detail_info in order_details:
        order_details = OrderDetails(None, detail_info[0], detail_info[1],
                                     detail_info[2], None)
        order.order_details.append(order_details)

    sql_connection = dbconnection.get_db_connection()
    order_repository.save_order(sql_connection, order)
    sql_connection.close()


def create_frame():
    root = Tkinter.Tk()
    root.eval('tk::PlaceWindow %s center' % root.winfo_pathname(root.winfo_id()))
    root.geometry('500x500')
    root.resizable(width=False, height=False)
    root.title("Order")

    lbl_title = Tkinter.Label(root, text="__ORDER__")
    lbl_title.place(x=225, y=1)

    lbl_customer = Tkinter.Label(root, text="Customer Name: ")
    lbl_customer.place(x=20, y=40)
    txt_customer = Tkinter.Entry(root, width=40)
    txt_customer.place(x=150, y=40)

    lbl_date = Tkinter.Label(root, text="Date: ")
    lbl_date.place(x=20, y=70)
    txt_date = Tkinter.Entry(root, width=40)
    txt_date.place(x=150, y=70)
    txt_date.insert(0, str(time.strftime("%Y-%m-%d")))

    lbl_customer_address = Tkinter.Label(root, text="Customer Address: ")
    lbl_customer_address.place(x=20, y=100)
    txt_customer_address = Tkinter.Entry(root, width=40)
    txt_customer_address.place(x=150, y=100)

    lbl_customer_phone = Tkinter.Label(root, text="Customer Phone: ")
    lbl_customer_phone.place(x=20, y=130)
    txt_customer_phone = Tkinter.Entry(root, width=40)
    txt_customer_phone.place(x=150, y=130)

    lbl_purchase_price = Tkinter.Label(root, text="Purchase Price: ")
    lbl_purchase_price.place(x=20, y=160)
    txt_purchase_price = Tkinter.Entry(root, width=40)
    txt_purchase_price.place(x=150, y=160)

    lbl_note = Tkinter.Label(root, text="Note: ")
    lbl_note.place(x=20, y=190)
    txt_note = ScrolledText.ScrolledText(wrap=Tkinter.WORD, height=5, width=40)
    txt_note.place(x=150, y=190)

    lbl_order_details = Tkinter.Label(root, text="__ORDER DETAILS__")
    lbl_order_details.place(x=190, y=300)

    lbl_num_articles = Tkinter.Label(root, text="Num Articles ")
    lbl_num_articles.place(x=20, y=330)

    lbl_description = Tkinter.Label(root, text="Description ")
    lbl_description.place(x=190, y=330)

    lbl_unit_price = Tkinter.Label(root, text="Unit Price ")
    lbl_unit_price.place(x=350, y=330)

    txt_num_articles = Tkinter.Entry(root, width=15)
    txt_num_articles .place(x=20, y=360)

    txt_description = Tkinter.Entry(root, width=15)
    txt_description .place(x=190, y=360)

    txt_unit_price = Tkinter.Entry(root, width=15)
    txt_unit_price  .place(x=350, y=360)

    order_details_list = list()

    def clear_fields():
        clear_details()
        txt_customer.delete(0, 'end')
        txt_customer_address.delete(0, 'end')
        txt_customer_phone.delete(0, 'end')
        txt_purchase_price.delete(0, 'end')
        txt_note.delete(1.0, Tkinter.END)
        txt_num_articles.delete(0, 'end')
        txt_description.delete(0, 'end')
        txt_unit_price.delete(0, 'end')

    def is_invalid_data():
        if len(order_details_list) == 0:
            return "Please insert a order detail"
        if not txt_customer.get():
            return "Please insert a customer name"
        if not txt_date.get():
            return "Please insert a valid date"
        if not txt_purchase_price:
            return "Please insert a valid purchase price"
        return False

    def save_action():
        result = tkMessageBox.askquestion("Validate Details info", order_details_list)
        if result == "yes":
            message = is_invalid_data()
            if message:
                tkMessageBox.showinfo("Message", message)
                return
            _save_order(txt_customer.get(),
                        int(datetime.datetime.strptime(txt_date.get(),
                                                       '%Y-%m-%d').strftime("%s")),
                        txt_customer_address.get(),
                        txt_customer_phone.get(),
                        txt_purchase_price.get(),
                        txt_note.get(1.0, Tkinter.END), order_details_list)
            tkMessageBox.showinfo("Message", "save data ok!")
            clear_fields()

    def new_order_detail_action():
        order_details_list.append((txt_num_articles.get(), txt_description.get(),
                                   txt_unit_price.get()))
        txt_num_articles.delete(0, 'end')
        txt_description.delete(0, 'end')
        txt_unit_price.delete(0, 'end')
        txt_num_articles.focus()

    def clear_details():
        del order_details_list[:]

    def query_order():
        query_order_window.create_frame()

    def payments():
        payments_window.create_frame()

    btn_save = Tkinter.Button(text="Save Order", command=save_action)
    btn_save.place(x=20, y=420)

    btn_query_order = Tkinter.Button(text="Query Order", command=query_order)
    btn_query_order.place(x=120, y=420)

    btn_payments = Tkinter.Button(text="Payments", command=payments)
    btn_payments.place(x=225, y=420)

    btn_new_order_detail = Tkinter.Button(text="+", command=new_order_detail_action)
    btn_new_order_detail.place(x=450, y=290)

    btn_clear_details = Tkinter.Button(text="Clear Details", command=clear_details)
    btn_clear_details.place(x=20, y=290)

    root.mainloop()
