# step1_explore_data.py
# STEP 1: LOAD AND EXPLORE DATA

import pandas as pd
import os

# Path to the folder where CSVs are
folder_path = "./data"  # relative path to your 'data' folder

# Load datasets
orders = pd.read_csv(os.path.join(folder_path, "olist_orders_dataset.csv"))
customers = pd.read_csv(os.path.join(folder_path, "olist_customers_dataset.csv"))
order_items = pd.read_csv(os.path.join(folder_path, "olist_order_items_dataset.csv"))
payments = pd.read_csv(os.path.join(folder_path, "olist_order_payments_dataset.csv"))
reviews = pd.read_csv(os.path.join(folder_path, "olist_order_reviews_dataset.csv"))
products = pd.read_csv(os.path.join(folder_path, "olist_products_dataset.csv"))
sellers = pd.read_csv(os.path.join(folder_path, "olist_sellers_dataset.csv"))
geolocation = pd.read_csv(os.path.join(folder_path, "olist_geolocation_dataset.csv"))
category_translation = pd.read_csv(os.path.join(folder_path, "product_category_name_translation.csv"))

print("All datasets loaded successfully!\n")

# Helper function to explore a dataset
def overview(df, name):
    print(f"\n--- {name} ---")
    print("First 3 rows:")
    print(df.head(3))
    print("\nInfo:")
    print(df.info())
    print("\nMissing values:")
    print(df.isnull().sum())

# Explore datasets
overview(orders, "Orders")
overview(customers, "Customers")
overview(order_items, "Order Items")
overview(payments, "Payments")
overview(reviews, "Reviews")
overview(products, "Products")
overview(sellers, "Sellers")
overview(geolocation, "Geolocation")
overview(category_translation, "Category Translation")

# Example join: orders + customers
orders_customers = orders.merge(customers, on="customer_id", how="left")
print("\n--- Sample merged Orders + Customers ---")
print(orders_customers.head(5))
