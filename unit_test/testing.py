import unittest
from dao.order_processor_repository import OrderProcessorRepository
from entity.model import Customer, Product, Cart, Order, Order_items
from exceptions import CustomerNotFoundException, ProductNotFoundException, OrderNotFoundException

class TestOrderProcessorRepository(unittest.TestCase):
    def test_create_customer(self):
        order_processor_repository = OrderProcessorRepository()
        customer = Customer.Customer(1, "John", "john@example.com", "password")
        self.assertTrue(order_processor_repository.create_customer(customer))

    def test_create_product(self):
        order_processor_repository = OrderProcessorRepository()
        product = Product.Product(1, "Product A", 10.99, "Description of Product A", 100)
        self.assertTrue(order_processor_repository.create_product(product))

    def test_delete_product(self):
        order_processor_repository = OrderProcessorRepository()
        product_id = 1
        self.assertTrue(order_processor_repository.delete_product(product_id))

    def test_add_to_cart(self):
        order_processor_repository = OrderProcessorRepository()
        customer = Customer.Customer(6, "John", "john@example.com", "password")
        product = Product.Product(6, "Product A", 10.99, "Description of Product A", 100)
        self.assertTrue(order_processor_repository.add_to_cart(customer, product, 10,2))

    def test_remove_from_cart(self):
        order_processor_repository = OrderProcessorRepository()
        customer = Customer.Customer(1, "John", "john@example.com", "password")
        product = Product.Product(1, "Product A", 10.99, "Description of Product A", 100)
        self.assertTrue(order_processor_repository.remove_from_cart(customer, product))

    def test_get_all_from_cart(self):
        order_processor_repository = OrderProcessorRepository()
        customer = Customer.Customer(1, "John", "john@example.com", "password")
        cart_items = order_processor_repository.get_all_from_cart(customer)
        self.assertGreater(len(cart_items), 0)

    def test_place_order(self):
        order_processor_repository = OrderProcessorRepository()
        customer = Customer.Customer(1, "John", "john@example.com", "password")
        order_items = [(Product.Product(1, "Product A", 10.99, "Description of Product A", 100))]
        shipping_address = "123 Street, City"
        self.assertTrue(order_processor_repository.place_order(customer, order_items, shipping_address))

    def test_get_orders_by_customer(self):
        order_processor_repository = OrderProcessorRepository()
        customer_id = 1
        orders = order_processor_repository.get_orders_by_customer(customer_id)
        self.assertGreater(len(orders), 0)

if __name__ == "__main__":
    unittest.main()