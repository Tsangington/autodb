import psycopg2
import datetime 
from datetime import datetime
import pandas as pd

class Database:
    def __init__(self, name, user, password, host, port):
        self.conn = psycopg2.connect(dbname=name, user=user, password=password, host=host, port=port)
        self.create_tables()
        self.import_initial_data()

    def create_tables(self):
        with self.conn.cursor() as cursor:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS customer (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS customer_order (
                id SERIAL PRIMARY KEY,
                customer_id INT REFERENCES customer(id) ON DELETE CASCADE,
                order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                price DECIMAL(10, 2)
            )
            """)
        self.conn.commit()

    def import_initial_data(self):
        try:
            customers_df = pd.read_csv("static/csv/example_customers.csv")
            for _, row in customers_df.iterrows():
                name = row['name']
                created_at = row.get('created_at', None)
                if pd.isna(created_at):
                    created_at = None
                self.store_customer(name, created_at)
            print("Customers imported successfully.")
        except Exception as e:
            print(f"Failed to import customers: {e}")

        try:
            orders_df = pd.read_csv("static/csv/example_orders.csv")
            for _, row in orders_df.iterrows():
                customer_id = int(row['customer_id'])
                price = float(row['price'])
                order_date = row.get('order_date', None)
                if pd.isna(order_date):
                    order_date = None
                self.store_order(customer_id, price, order_date)
            print("Orders imported successfully.")
        except Exception as e:
            print(f"Failed to import orders: {e}")

    def store_customer(self, name, created_at=None):
        with self.conn.cursor() as cursor:
            if created_at:
                if isinstance(created_at, str):
                    created_at = datetime.fromisoformat(created_at)
                cursor.execute(
                    "INSERT INTO customer (name, created_at) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                    (name, created_at)
                )
            else:
                cursor.execute(
                    "INSERT INTO customer (name) VALUES (%s) ON CONFLICT DO NOTHING",
                    (name,)
                )
            self.conn.commit()
        return "successful insert into customer table!"

    def store_order(self, customer_id, price, order_date=None):
        with self.conn.cursor() as cursor:
            if order_date:
                if isinstance(order_date, str):
                    order_date = datetime.fromisoformat(order_date)
                cursor.execute(
                    "INSERT INTO customer_order (id, price, order_date) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
                    (customer_id, price, order_date)
                )
            else:
                cursor.execute(
                    "INSERT INTO customer_order (id, price) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                    (customer_id, price)
                )
            self.conn.commit()
        return "successful insert into order table!"

    def get_customers(self):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT id, name, created_at FROM customer")
            rows = cursor.fetchall()
        return rows

    def get_orders(self):
        with self.conn.cursor() as cursor:
            cursor.execute("""
            SELECT id, customer_id, order_date, price 
            FROM customer_order
            """)
            rows = cursor.fetchall()
        return rows
        
    def get_data(self):
        with self.conn.cursor() as cursor:
            cursor.execute("""
            SELECT customer_order.id as order_id, customer_id, order_date, customer.name, price
            FROM customer_order
            JOIN customer ON customer.id = customer_order.customer_id
            """)
            rows = cursor.fetchall()
        return rows

    def close(self):
        self.conn.close()
