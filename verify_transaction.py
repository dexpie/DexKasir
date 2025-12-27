from models.transaction import TransactionModel
from models.product import ProductModel
from database.db import Database
import os

# Setup
if os.path.exists("kasir.db"):
    print("Using existing kasir.db")

db = Database("kasir.db")
db.init_db()

# Ensure we have a product
pm = ProductModel()
pm.add_product("Test Prod", 10000, 100, "12345")
products = pm.get_all_products()
p = products[0]
print(f"Product: {p}")

# Test Transaction
tm = TransactionModel()
items = [{
    'product_id': p['id'],
    'name': p['name'],
    'price': p['price'],
    'qty': 1,
    'subtotal': p['price']
}]

print("Attempting to create transaction...")
success = tm.create_transaction(
    cashier_name="admin",
    items=items,
    subtotal=10000,
    discount=0,
    tax=1000,
    final_total=11000,
    payment_method="CASH"
)

if success:
    print("Transaction Success!")
else:
    print("Transaction Failed!")
