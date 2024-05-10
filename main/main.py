from dao.order_processor_repository import OrderProcessorRepository
from entity.model import Customer, Product, Cart, Order, Order_items
from exceptions import CustomerNotFoundException, ProductNotFoundException, OrderNotFoundException

class MainModule:
    def __init__(self):
        self.order_processor_repository = OrderProcessorRepository()

    def run(self):
        while True:
            print("Ecommerce Application Menu:")
            print("1. Register Customer")
            print("2. Create Product")
            print("3. Delete Product")
            print("4. Add to Cart")
            print("5. View Cart")
            print("6. Place Order")
            print("7. View Customer Order")
            print("8. Other options")
            print("9. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                customer_id=float(input("Enter the customer id: "))
                name = input("Enter customer name: ")
                email = input("Enter customer email: ")
                password = input("Enter customer password: ")
                customer = Customer.Customer(customer_id, name, email, password)
                if self.order_processor_repository.create_customer(customer):
                    print("Customer registered successfully.")
                else:
                    print("Error registering customer.")
            elif choice == "2":
                product_id = int(input("Enter the product id: "))
                name = input("Enter product name: ")
                price = int(input("Enter product price: "))
                description = input("Enter product description: ")
                stock_quantity = int(input("Enter product stock quantity: "))
                product = Product.Product(product_id, name, price, description, stock_quantity)
                if self.order_processor_repository.create_product(product):
                    print("Product created successfully.")
                else:
                    print("Error creating product.")
            elif choice == "3":
                product_id = int(input("Enter product ID to delete: "))
                if self.order_processor_repository.delete_product(product_id):
                    print("Product deleted successfully.")
                else:
                    print("ProductNotFoundException: Product is not present")
            elif choice == "4":
                cart_id = int(input("Enter cart ID: "))
                customer_id = int(input("Enter customer ID: "))
                product_id = int(input("Enter product ID: "))
                quantity = int(input("Enter quantity: "))
                try:
                    cart=Cart.Cart(cart_id,"","","")
                    customer = Customer.Customer(customer_id, "", "", "")
                    product = Product.Product(product_id, "", 0, "", 0)
                    if self.order_processor_repository.add_to_cart(cart,customer, product, quantity):
                        print("Product added to cart successfully.")
                    else:
                        print("Error adding product to cart.")
                except (CustomerNotFoundException, ProductNotFoundException) as e:
                    print("CustomerNotFoundException",str(e))
            elif choice == "5":
                customer_id = int(input("Enter customer ID: "))
                try:
                    customer = Customer.Customer(customer_id, "", "", "")
                    cart_items = self.order_processor_repository.get_all_from_cart(customer)
                    if cart_items:
                        print("Cart Items:")
                        for product_id, name, price, quantity in cart_items:
                            print(f"Product ID: {product_id}, Name: {name}, Price: {price}, Quantity: {quantity}")
                    else:
                        print("Cart is empty.")
                except CustomerNotFoundException as e:
                    print(str(e))
            elif choice == "6":
                order_id =int(input("Enter the order id: "))
                customer_id = int(input("Enter customer ID: "))
                shipping_address = input("Enter shipping address: ")
                try:
                    customer = Customer.Customer(customer_id, "", "", "")
                    cart_items = self.order_processor_repository.get_all_from_cart(customer)
                    order_items = ((Product.Product(product_id, name, price, "", 0), quantity) for product_id, name, price, quantity in cart_items)
                    if self.order_processor_repository.place_order(order_id,order_id,customer, order_items, shipping_address):
                        print("Order placed successfully.")
                    else:
                        print("CustomerNotFoundException : Customer is not present")
                except (CustomerNotFoundException, ProductNotFoundException) as e:
                    print(str(e))
            elif choice == "7":
                customer_id = int(input("Enter customer ID: "))
                try:
                    orders = self.order_processor_repository.get_orders_by_customer(customer_id)
                    if orders:
                        print("Customer Orders:")
                        for order_id, order_date, total_price, shipping_address, product_id, product_name, quantity in orders:
                            print(f"Order ID: {order_id}, Order Date: {order_date}, Total Price: {total_price}, Shipping Address: {shipping_address}")
                            print(f"Product ID: {product_id}, Product Name: {product_name}, Quantity: {quantity}")
                            print("---")
                    else:
                        print("CustomerNotFoundException : Customer is not present")
                except CustomerNotFoundException as e:
                    print(str(e))

            elif choice == "8":
                while True:
                    print("1. Update Customer")
                    print("2. Delete Customer")
                    print("3. Update Product")
                    print("4. Update Cart")
                    print("5. Update Order")
                    print("6. Delete Order")
                    print("7. Update order items")
                    print("8. Delete order items")
                    print("9. Go back to Main Menu")
                    choice = input("Enter your choice: ")

                    if choice == "1":
                        self.order_processor_repository.update_customer_by_id()

                    elif choice =="2":
                        self.order_processor_repository.delete_customer()

                    elif choice =="3":
                        self.order_processor_repository.update_product_by_id()

                    elif choice =="4":
                        self.order_processor_repository.update_cart()

                    elif choice == "5":
                        self.order_processor_repository.update_order()

                    elif choice =="6":
                        self.order_processor_repository.delete_order()

                    elif choice =="7":
                        self.order_processor_repository.update_order_item()

                    elif choice =="8":
                        self.order_processor_repository.delete_order_item()

                    elif choice == "9":
                        break

                    else:
                        print("Invalid choice. Please try again.")



            elif choice == "9":
                print("Thanks for using our E-Commerce Program")
                break
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main_module = MainModule()
    main_module.run()