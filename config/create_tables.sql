-- Describe TBL_ORDER
CREATE TABLE tbl_order (
    "id" INTEGER NOT NULL primary key autoincrement,
    "customer" TEXT NOT NULL,
    "date" INTEGER NOT NULL,
    "customer_address" TEXT,
    "purchase_price" INTEGER NOT NULL,
    "customer_phone" TEXT,
    "note" TEXT
)

-- Describe TBL_ORDER_DETAILS
CREATE TABLE "tbl_order_details"
(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    num_articles INTEGER NOT NULL,
    description TEXT NOT NULL,
    unit_price INTEGER NOT NULL,
    order_id INTEGER NOT NULL,
    FOREIGN KEY (order_id) REFERENCES tbl_order(id)
)

-- Describe TBL_PAYMENT
CREATE TABLE tbl_payment
(
    id integer primary key autoincrement not null,
    order_id integer not null,
    date integer not null,
    amount integer not null,
    FOREIGN KEY(order_id) REFERENCES tbl_order(id)
)