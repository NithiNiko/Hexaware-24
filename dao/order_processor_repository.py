from entity.model import Customer, Product, Cart, Order, Order_items
from exceptions import CustomerNotFoundException, ProductNotFoundException, OrderNotFoundException
from util.db_conn_util import DBConnectivity

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

    def delete_customer(self, customer_id):
        try:
            conn = self.db_conn_util.makeconnection()
            cursor = conn.cursor()
            sql = "DELETE FROM customers WHERE customer_id = %s"
            cursor.execute(sql, (customer_id,))
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

    def place_order(self, order_id,customer, order_items, shipping_address):
        try:
            conn = self.db_conn_util.makeconnection()
            cursor = conn.cursor()

            # Insert order
            sql = "INSERT INTO Orders (order_id,customer_id, order_date, total_price, shipping_address) VALUES (%s,%s, NOW(), %s, %s)"
            total_price = sum(item[1] * item[2] for item in order_items)
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