import sqlite3
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_name="inventory.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Products table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                price REAL,
                quantity INTEGER,
                sold_quantity INTEGER
            )
        """)
        # Sales table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER,
                quantity_sold INTEGER,
                total_price REAL,
                date TEXT,
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            )
        """)
        self.conn.commit()

    def add_or_update_product(self, name, price, quantity):
        # Check if product exists
        self.cursor.execute("SELECT * FROM products WHERE name=?", (name,))
        product = self.cursor.fetchone()
        if product:
            # Update quantity
            new_quantity = product[3] + quantity
            self.cursor.execute("UPDATE products SET quantity=? WHERE name=?", (new_quantity, name))
        else:
            # Insert new product
            self.cursor.execute("INSERT INTO products (name, price, quantity, sold_quantity) VALUES (?, ?, ?, ?)",
                                (name, price, quantity, 0))
        self.conn.commit()

    def record_sale(self, name, quantity, total_price):
        # Get product ID and current sold quantity
        self.cursor.execute("SELECT product_id, sold_quantity, quantity FROM products WHERE name=?", (name,))
        product = self.cursor.fetchone()
        if not product:
            print(f"Product {name} not found in DB!")
            return
        product_id, sold_quantity, current_quantity = product
        # Update quantity and sold_quantity
        new_sold = sold_quantity + quantity
        new_quantity = current_quantity - quantity
        self.cursor.execute("UPDATE products SET quantity=?, sold_quantity=? WHERE product_id=?",
                            (new_quantity, new_sold, product_id))
        # Insert into sales table
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute("INSERT INTO sales (product_id, quantity_sold, total_price, date) VALUES (?, ?, ?, ?)",
                            (product_id, quantity, total_price, date))
        self.conn.commit()

    def get_inventory(self):
        self.cursor.execute("SELECT name, price, quantity, sold_quantity FROM products")
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()


##########################################
# Conneting Database with inventory
class Inventory:
    def __init__(self):
        self.db = DatabaseManager()
        self.total_cash = 0

    def add_product(self, name, price, quantity):
        self.db.add_or_update_product(name, price, quantity)
        print(f"Product added/restocked: {name} - {quantity} units at {price} each.")

    def sell_product(self, name, quantity):
        # Get product info from DB
        products = self.db.get_inventory()
        product_dict = {p[0]: p for p in products}  # name -> tuple
        if name not in product_dict:
            print(f"Product {name} not found!")
            return
        price = product_dict[name][1]
        stock = product_dict[name][2]
        if quantity > stock:
            print(f"Not enough stock! Available: {stock}")
            return
        total_price = price * quantity
        self.total_cash += total_price
        self.db.record_sale(name, quantity, total_price)
        print(f"Sold {quantity} {name}(s) for {total_price} currency units.")

    def get_summary(self):
        products = self.db.get_inventory()
        print("\n--- Inventory Summary ---")
        for p in products:
            print(f"{p[0]}: Price={p[1]}, In stock={p[2]}, Sold={p[3]}")
        print(f"Total cash earned: {self.total_cash} currency units")
        print("-------------------------\n")

    def close(self):
        self.db.close()

