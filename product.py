class Product:
    def __init__(self,name,price,quantity):
        """
        Docstring for __init__
        
        Intitialize a new product
        :param name: string of product name
        :param price: float of the product price
        :param quantity: integer for the number of product
        """
        self.name = name
        self.price = price
        self.quantity = quantity
        self.sold_quantity = 0
    
    def sell(self, amount):
        """
        Docstring for sell
        
        Sell a certain number of product
        update is quantity and sold quantity
        :param amount: integer for the number of product sold
        return total price of the sold product
        """

        if amount > self.quantity:
            print(f"Not enough {self.name} in stock! Available: {self.quantity}")
            return 0 
        self.quantity -= amount
        self.sold_quantity += amount
        total_price = amount * self.price
        print(f"Sold {amount} {self.name}(s) for {total_price} currency units.")
        return total_price
    
    def restock(self, amount):
        """
        Docstring for restock
        
        Add quantity to stock.
        :param amount: integer for the number of products added
        """
        self.quantity += amount
        print(f"Restocked {amount} {self.name}(s). Current stock: {self.quantity}")

    def __str__(self):
        """
        Docstring for __str__
        
        :print product info
        """
        return f"{self.name}: Price={self.price}, In stock={self.quantity}, Sold={self.sold_quantity}"
    
class Inventory:
    def __init__(self):
        """
        Docstring for __init__
        
        :initialize an empty inventory.
        """
        self.products = {} #key: product name, value:product object
        self.total_cash = 0
        # self.db = DatabaseManager("inventory.db")


    def add_product(self, name, price, quantity):
        """
        add new or restock product
        """
        if name in self.products:
            self.products[name].restock(quantity)
        else:
            self.products[name] = Product(name, price, quantity)
            print(f"Added new product: {name} -- {quantity} units at ${price}")

            #save data immediately for persistent
            self.db.add_or_update_product(name, price, quantity)
    
    def sell_product(self, name, quantity):
        """
        Sell a product if it exists in inventory.
        """
        if name not in self.products:
            print(f"Product {name} does not exist!")
            return
        total_price = self.products[name].sell(quantity)
        self.total_cash += total_price
       
        #Record the sale in the database
        self.db.record_sale(name, quantity, total_price)
    
    def get_summary(self):
        """
         print full inventory
        """

        print("\n----- Inventory Summary ----")
        for product in self.products.values():
            print(product)
        print(f"Total cash earned: {self.total_cash} currency units")
        print("-----------------------------\n")
    
    def save_to_db(self, db_manager):
        """
        Docstring for save_to_db
        
        This takes my object data and writes it to SQLite
        """
        for product in self.products.values():
         db_manager.add_or_update_product(product.name,product.price,product.quantity)
        print("All products saved to database successfully.")



my_inventory = Inventory()

my_inventory.add_product("Soap", 50, 20)

my_inventory.sell_product("Soap", 5)

my_inventory.add_product("Sufuria", 100, 7)
my_inventory.sell_product("Sufuria", 3)
