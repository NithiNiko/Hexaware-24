class Cart:
    def __init__(self, cart_id, customer_id, product_id, quantity):
        self.cart_id = cart_id
        self.customer_id = customer_id
        self.product_id = product_id
        self.quantity = quantity

    def get_cart_id(self):
        return self.cart_id

    def get_customer_id(self):
        return self.customer_id

    def get_product_id(self):
        return self.product_id

    def get_quantity(self):
        return self.quantity