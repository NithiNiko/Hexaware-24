from entity.model import Customer, Product, Cart, Order, Order_items
from exceptions import CustomerNotFoundException, ProductNotFoundException, OrderNotFoundException
from util.db_conn_util import DBConnectivity
import time
class OrderProcessorRepository:
    def __init__(self):
        self.db_conn_util = DBConnectivity()

    def create_product(self, product):
        try:
            conn = self.db_conn_util.makeconnection()
            if conn is None:
                raise Exception("Db connnection failed")
            cursor = conn.cursor()
            sql = "INSERT INTO products (product_id,name, price, description, stock_quantity) VALUES (%s,%s, %s, %s, %s)"
            values = (product.get_product_id(),product.get_name(), product.get_price(), product.get_description(), product.get_stock_quantity())
            cursor.execute(sql, values)
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error creating product: {e}")
            return False

    def update_product_by_id(self):
        conn = self.db_conn_util.makeconnection()
        cursor = conn.cursor()
        self.product_id = int(input("Enter the product id: "))
        self.name = input("Enter product name: ")
        self.price = int(input("Enter product email: "))
        self.description = input("Enter product password: ")
        self.stock_quantity=int(input("Enter the stock qunatity: "))
        cursor.execute( "UPDATE products set name =%s,price= %s, description=%s, stock_quantity=%s where customer_id=%s",
                        (self.name,self.price,self.description,self.stock_quantity,self.customer_id))
        print("Product updated successfully")
        conn.commit()
        conn.close()

    def create_customer(self, customer):
        try:
            conn = self.db_conn_util.makeconnection()
            if conn is None:
                raise Exception("Db connnection failed")
            cursor = conn.cursor()
            sql = "INSERT INTO Customer (customer_id,name, email, password) VALUES (%s,%s, %s, %s)"
            values = (customer.get_customer_id(),customer.get_name(), customer.get_email(), customer.get_password())
            cursor.execute(sql, values)
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error creating customer: {e}")
            return False
        
    def update_customer_by_id(self):
        conn = self.db_conn_util.makeconnection()
        cursor = conn.cursor()
        self.customer_id = int(input("Enter the customer id: "))
        self.name = input("Enter customer name: ")
        self.email = input("Enter customer email: ")
        self.password = input("Enter customer password: ")
        cursor.execute( "UPDATE customer set name =%s,email = %s,password= %s where customer_id=%s",
                        (self.name,self.email,self.password,self.customer_id))
        print("Customer updated successfully")
        conn.commit()
        conn.close()

    def delete_product(self, product_id):
        try:
            conn = self.db_conn_util.makeconnection()
            cursor = conn.cursor()
            sql = "DELETE FROM products WHERE product_id = %s"
            cursor.execute(sql, (product_id,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting product: {e}")
            return False

    def delete_customer(self):
        try:
            conn = self.db_conn_util.makeconnection()
            cursor = conn.cursor()
            self.customer_id=int(input("Enter the customer id to delete:"))
            sql = "DELETE FROM customer WHERE customer_id = %s"
            cursor.execute(sql, (self.customer_id,))
            print("Customer deleted successfully..")
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting customer: {e}")
            return False

    def add_to_cart(self, cart,customer, product, quantity):
        try:
            conn = self.db_conn_util.makeconnection()
            cursor = conn.cursor()
            sql = "INSERT INTO cart (cart_id,customer_id, product_id, quantity) VALUES (%s,%s, %s, %s)"
            values = (cart.get_cart_id(),customer.get_customer_id(), product.get_product_id(), quantity)
            cursor.execute(sql, values)
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error adding to cart: {e}")
            return False

    def remove_from_cart(self, customer, product):
        try:
            conn = self.db_conn_util.makeconnection()
            cursor = conn.cursor()
            sql = "DELETE FROM cart WHERE customer_id = %s AND product_id = %s"
            values = (customer.get_customer_id(), product.get_product_id())
            cursor.execute(sql, values)
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error removing from cart: {e}")
            return False

    def update_cart(self):
        self.cart_id = int(input('Enter cart_id that has to be updated:'))
        self.customer_id = int(input('enter customer_id: '))
        self.product_id = int(input('Enter product_id:'))
        self.quantity = int(input('quantity:'))
        cursor.execute("UPDATE cart set customer_id=%s, product_id=%s, quantity=%s where cart_id=%s",
                       (self.cart_id, self.product_id, self.quantity, self.cart_id))
        print("Cart updated successfully")
        conn.commit()
        conn.close()

    def get_all_from_cart(self, customer):
        try:
            conn = self.db_conn_util.makeconnection()
            cursor = conn.cursor()
            sql = "SELECT p.product_id, p.name, p.price, c.quantity FROM cart c JOIN products p ON c.product_id = p.product_id WHERE c.customer_id = %s"
            cursor.execute(sql, (customer.get_customer_id(),))
            cart_items = cursor.fetchall()
            cursor.close()
            conn.close()
            return cart_items
        except Exception as e:
            print(f"Error getting cart items: {e}")
            return ()

    def place_order(self, order_item_id,order_id,customer, order_items, shipping_address):
        try:
            conn = self.db_conn_util.makeconnection()
            cursor = conn.cursor()
            # Insert order items
            for product, quantity in order_items:
                sql = "INSERT INTO order_items (order_item_id,order_id, product_id, quantity) VALUES (%s,%s, %s, %s)"
                cursor.execute(sql, (order_item_id,order_id, product.get_product_id(), quantity))

            # Insert order
            total_price=product.get_price()
            sql = "INSERT INTO Orders (order_id,customer_id, order_date, total_price, shipping_address) VALUES (%s,%s, NOW(), %s, %s)"
            #total_price = sum(item[1] * item[2] for item in order_items)
            cursor.execute(sql, (order_id,customer.get_customer_id(), total_price, shipping_address))
            order_id = cursor.lastrowid

            # Insert order items
            for product, quantity in order_items:
                sql = "INSERT INTO order_items (order_id, product_id, quantity) VALUES (%s, %s, %s)"
                cursor.execute(sql, (order_id, product.get_product_id(), quantity))

            # Commit changes
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error placing order: {e}")
            return False

    def update_order(self):
        self.order_id = int(input('Enter order_id that has to be updated:'))
        self.customer_id = int(input('Enter customer_id: '))
        self.order_date = int(input('Enter order date that has to be updated:'))
        self.total_price= int(input('Enter the updated price:'))
        self.shipping_address= input("Enter the new shipping address: ")
        cursor.execute("UPDATE orders set  customer_id=%s, order_date=%s, total_price=%s, shipping address where order_id=%s",
                       (self.customer_id, self.order_date, self.total_price, self.shipping_address,self.order_id))
        print("Order updated successfully")
        conn.commit()
        conn.close()

    def delete_order(self):
        self.order_id = int(input('enter the order_id to be deleted:'))
        cursor.execute("DELETE from orders where order_id=%s",
                       (self.order_id))
        print("Order deleted successfully")
        conn.commit()
        conn.close()

    def update_order_item(self):
        self.order_item_id = int(input('Enter order_item_id which is to be updated:'))
        self.order_id = int(input('Enter order_id:'))
        self.product_id = int(input('Enter product_id: '))
        self.quantity = int(input("quantity: "))
        cursor.execute("update order_items set order_id =%s,product_id = %s,quantity=%s where order_item_id = %s",
                       (self.order_id,self.product_id,self.quantity,self.order_item_id))
        print("Order items updated successfully")
        conn.commit()
        conn.close()

    def delete_order_item(self):
        self.order_item_id = int(input('enter the order_item_id to be deleted:'))
        cursor.execute("delete from order_items where order_item_id=%s",
                       (self.order_item_id))
        print("Order items deleted successfully")
        conn.commit()
        conn.close()

    def get_orders_by_customer(self, customer_id):
        try:
            conn = self.db_conn_util.makeconnection()
            cursor = conn.cursor()
            sql = "SELECT o.order_id, o.order_date, o.total_price, o.shipping_address, p.product_id, p.name, oi.quantity FROM Orders o JOIN Order_items oi ON o.order_id = oi.order_id JOIN Products p ON oi.product_id = p.product_id WHERE o.customer_id = %s"
            cursor.execute(sql, (customer_id,))
            orders = cursor.fetchall()
            cursor.close()
            conn.close()
            return orders
        except Exception as e:
            print(f"Error getting orders by customer: {e}")
            return ()
