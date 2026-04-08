# step2_clean_prepare_data.py
# STEP 2: DATA CLEANING & BUSINESS PREPARATION

import pandas as pd
import os

# -----------------------------
# 1. LOAD DATA
# -----------------------------
folder_path = "./data"

orders = pd.read_csv(os.path.join(folder_path, "olist_orders_dataset.csv"))
order_items = pd.read_csv(os.path.join(folder_path, "olist_order_items_dataset.csv"))
customers = pd.read_csv(os.path.join(folder_path, "olist_customers_dataset.csv"))
products = pd.read_csv(os.path.join(folder_path, "olist_products_dataset.csv"))
category_translation = pd.read_csv(
    os.path.join(folder_path, "product_category_name_translation.csv")
)

print("Datasets loaded successfully!")


# -----------------------------
# 2. FILTER ONLY DELIVERED ORDERS
# -----------------------------
orders = orders[orders["order_status"] == "delivered"]
print(f"Orders after filtering delivered: {orders.shape}")

# Business reasoning:
# Only delivered orders generate revenue.
# Cancelled / unavailable orders are ignored.

# -----------------------------
# 3. CONVERT DATE COLUMNS
# -----------------------------
date_columns = [
    "order_purchase_timestamp",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]

for col in date_columns:
    orders[col] = pd.to_datetime(orders[col], errors="coerce")

print("Date columns converted to datetime.")

# -----------------------------
# 4. CREATE TIME-BASED COLUMNS
# -----------------------------
orders["order_year"] = orders["order_purchase_timestamp"].dt.year
orders["order_month"] = orders["order_purchase_timestamp"].dt.month
orders["order_month_name"] = orders["order_purchase_timestamp"].dt.month_name()

print("Time-based columns created.")
print("**********Example**********")
print(orders.head(2))

# -----------------------------
# 5. CALCULATE REVENUE PER ORDER
# -----------------------------
# Revenue = sum(price + freight) per order

order_items["total_item_value"] = (
    order_items["price"] + order_items["freight_value"]
)

revenue_per_order = (
    order_items.groupby("order_id")["total_item_value"]
    .sum()
    .reset_index()
    .rename(columns={"total_item_value": "order_revenue"})
)

print("Revenue calculated per order.")

# -----------------------------
# 6. MERGE DATA INTO ONE FACT TABLE
# -----------------------------
fact_orders = (
    orders.merge(revenue_per_order, on="order_id", how="left")
          .merge(customers, on="customer_id", how="left")
)

print("Fact table created.")

# -----------------------------
# 7. CLEAN PRODUCT CATEGORY NAMES
# -----------------------------
products = products.merge(
    category_translation,
    on="product_category_name",
    how="left"
)

print("Product categories translated to English.")
print(products['product_category_name_english'].head(5))

# -----------------------------
# 8. FINAL CHECK
# -----------------------------
print("\nFinal fact_orders info:")
print(fact_orders.info())

print("\nSample rows from fact_orders:")
print(fact_orders.head(5))


