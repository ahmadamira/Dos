from flask_app  import app

CATALOG_ADDRESS = "http://flask_app_1:5000"
ORDER_ADDRESS = "http://flask_app_2:5001"

# Define a new Replication class
class CustomReplication:
    def __init__(self, catalog_addresses, order_addresses):
        self.catalog_addresses = catalog_addresses
        self.order_addresses = order_addresses
        self.catalog_address_turn = 0
        self.order_address_turn = 0

    def get_catalog_address(self):
        address = self.catalog_addresses[self.catalog_address_turn]
        self.catalog_address_turn = (self.catalog_address_turn + 1) % len(self.catalog_addresses)
        return address

    def get_order_address(self):
        address = self.order_addresses[self.order_address_turn]
        self.order_address_turn = (self.order_address_turn + 1) % len(self.order_addresses)
        return address

    def get_catalog_count(self):
        return len(self.catalog_addresses)

    def get_order_count(self):
        return len(self.order_addresses)


# Create an instance of the new Replication class
custom_replication = CustomReplication(CATALOG_ADDRESS, ORDER_ADDRESS)

# Define timeout values
custom_timeout = (0.2, 2.0)
