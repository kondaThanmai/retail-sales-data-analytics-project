# step3_export_for_sql.py
# PURPOSE: Export clean fact_orders table for SQL

import pandas as pd
import os

# Load raw data
folder_path = "./data"

orders = pd.read_csv(os.path.join(folder_path, "olist_orders_dataset.csv"))
order_items = pd.read_csv(os.path.join(folder_path, "olist_order_items_dataset.csv"))
customers = pd.read_csv(os.path.join(folder_path, "olist_customers_dataset.csv"))

# 1. Keep only delivered orders
orders = orders[orders["order_status"] == "delivered"]

# 2. Convert purchase timestamp to datetime
orders["order_purchase_timestamp"] = pd.to_datetime(
    orders["order_purchase_timestamp"]
)

# 3. Create time columns
orders["order_year"] = orders["order_purchase_timestamp"].dt.year
orders["order_month"] = orders["order_purchase_timestamp"].dt.month
orders["order_month_name"] = orders["order_purchase_timestamp"].dt.month_name()

# 4. Calculate revenue per order
order_items["total_item_value"] = (
    order_items["price"] + order_items["freight_value"]
)

revenue_per_order = (
    order_items
    .groupby("order_id")["total_item_value"]
    .sum()
    .reset_index()
    .rename(columns={"total_item_value": "order_revenue"})
)

# 5. Create fact table
fact_orders = (
    orders
    .merge(revenue_per_order, on="order_id", how="left")
    .merge(customers, on="customer_id", how="left")
)

# 6. Export to CSV
fact_orders.to_csv("fact_orders_for_sql.csv", index=False)

print("SUCCESS: fact_orders_for_sql.csv created")
