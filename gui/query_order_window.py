import ScrolledText
import Tkinter
import datetime
import tkMessageBox
from config import dbconnection
from order import order_repository
from order.order_exceptions import OrderIdNotFoundException


def create_frame():
    root = Tkinter.Tk()
    root.eval('tk::PlaceWindow %s center' % root.winfo_pathname(root.winfo_id()))
    root.geometry('500x500')
    root.resizable(width=False, height=False)
    root.title("Query")

    lbl_customer = Tkinter.Label(root, text="Customer Name: ")
    lbl_customer.place(x=20, y=40)
    txt_customer = Tkinter.Entry(root, width=25)
    txt_customer.place(x=150, y=40)

    def paint_orders(orders):
        for order in orders:
            readable_date = datetime.datetime.fromtimestamp(int(order.date)). \
                strftime('%Y-%m-%d')
            order_str = "order:{0} - customer:{1} - date:{2} - address:{3} - " \
                        "phone:{4} - note:{5}".format(order.id,
                                                      order.customer, readable_date,
                                                      order.customer_address,
                                                      order.customer_phone,
                                                      order.note)
            txt_query.insert(Tkinter.INSERT, order_str)
            txt_query.insert(Tkinter.INSERT, "\nORDER_DETAILS")
            total = [order_detail.num_articles * order_detail.unit_price
                     for order_detail in order.order_details]
            total = sum(total)
            for order_detail in order.order_details:
                order_detail_str = "\nnum Articles:{0} - description:{1} - " \
                                   "unit_price:{2}".format(order_detail.num_articles,
                                                           order_detail.description,
                                                           order_detail.unit_price)

                txt_query.insert(Tkinter.INSERT, order_detail_str)
            txt_query.insert(Tkinter.INSERT, "\nTotal price:%s" % total)
            txt_query.insert(Tkinter.INSERT, "\n---------------------------------\n")

    def query_order_by_customer_name():
        txt_query.delete(1.0, Tkinter.END)
        with dbconnection.get_db_connection() as sql_connection:
            orders = order_repository.get_orders_by_customer_name(
                sql_connection, txt_customer.get())
            paint_orders(orders)

    def query_order_by_order_id():
        txt_query.delete(1.0, Tkinter.END)
        with dbconnection.get_db_connection() as sql_connection:
            try:
                order = order_repository.get_order_by_order_id(
                    sql_connection, txt_order_id.get())
                paint_orders([order])
            except OrderIdNotFoundException as ex:
                tkMessageBox.showinfo("Error", ex.message)

    btn_query = Tkinter.Button(root, text="Query By Name",
                               command=query_order_by_customer_name)
    btn_query.place(x=370, y=40)

    lbl_order_id = Tkinter.Label(root, text="Order Id: ")
    lbl_order_id.place(x=20, y=90)
    txt_order_id = Tkinter.Entry(root, width=25)
    txt_order_id.place(x=150, y=90)

    btn_query_by_id = Tkinter.Button(root, text="Query By Id",
                                     command=query_order_by_order_id)
    btn_query_by_id.place(x=370, y=85)

    txt_query = ScrolledText.ScrolledText(root, wrap=Tkinter.WORD, height=25, width=62)
    txt_query.place(x=20, y=120)

    root.mainloop()
