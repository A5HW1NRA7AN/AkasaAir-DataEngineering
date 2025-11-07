# src/table_based/load_table.py
"""
Load cleaned and preprocessed dataframes into MySQL database.

This module is part of the TABLE-BASED APPROACH for the Akasa Air Data Engineering task.
Responsibilities:
  1. Create tables (customers, orders_fact, order_items) if they don't exist.
  2. Insert data from preprocessed DataFrames into these tables.
  3. Maintain referential integrity and ensure safe inserts.

Developer Notes:
  - Uses SQLAlchemy with pymysql driver.
  - The DB connection string is read from .env (via src.common.config).
  - Timestamps stored in UTC (as naive DATETIME).
"""

import pandas as pd
from sqlalchemy import text
from src.table_based.db import get_engine


# -------------------------------------------------------------
# STEP 1: Table Creation
# -------------------------------------------------------------
def create_tables():
    """
    Creates customers, orders_fact, and order_items tables if they don't already exist.
    Adds indexes for faster joins and KPI queries.
    """
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id VARCHAR(30) PRIMARY KEY,
            customer_name VARCHAR(100),
            mobile_number BIGINT UNIQUE,
            region VARCHAR(50)
        );
        """))

        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS orders_fact (
            order_id VARCHAR(30) PRIMARY KEY,
            mobile_number BIGINT,
            order_date_time_utc DATETIME,
            total_amount DECIMAL(10,2),
            INDEX (mobile_number),
            INDEX (order_date_time_utc),
            FOREIGN KEY (mobile_number) REFERENCES customers(mobile_number)
        );
        """))

        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS order_items (
            id INT AUTO_INCREMENT PRIMARY KEY,
            order_id VARCHAR(30),
            sku_id VARCHAR(30),
            sku_count INT,
            FOREIGN KEY (order_id) REFERENCES orders_fact(order_id)
        );
        """))

    print("[INFO] Tables verified/created successfully in MySQL.")


# -------------------------------------------------------------
# STEP 2: Insert DataFrames into MySQL
# -------------------------------------------------------------
def load_customers(customers_df: pd.DataFrame):
    """
    Inserts customer data into the customers table.
    Uses 'replace' mode to overwrite duplicates by primary key.
    """
    engine = get_engine()
    print("[INFO] Loading customers data into MySQL...")

    # Ensure consistent column order
    cols = ["customer_id", "customer_name", "mobile_number", "region"]
    customers_df = customers_df[cols].copy()

    customers_df.to_sql(
        name="customers",
        con=engine,
        if_exists="append",
        index=False,
        method="multi",
        chunksize=500
    )

    print(f"[SUCCESS] {len(customers_df)} customer rows loaded.")


def load_orders(fact_df: pd.DataFrame, raw_df: pd.DataFrame):
    """
    Loads order-level data (orders_fact) and line-item data (order_items).
    Deduplicates order IDs before inserting into orders_fact.
    """
    engine = get_engine()
    print("[INFO] Loading orders_fact and order_items data...")

    # 1. Prepare orders_fact dataframe
    fact_cols = ["order_id", "mobile_number", "order_date_time_utc", "total_amount"]
    fact_df = fact_df[fact_cols].drop_duplicates(subset=["order_id"]).copy()

    # Convert any timezone-aware datetime to naive UTC for MySQL
    if pd.api.types.is_datetime64tz_dtype(fact_df["order_date_time_utc"]):
        fact_df["order_date_time_utc"] = (
            fact_df["order_date_time_utc"]
            .dt.tz_convert("UTC")
            .dt.tz_localize(None)
        )

    # 2. Insert into orders_fact
    fact_df.to_sql(
        name="orders_fact",
        con=engine,
        if_exists="append",
        index=False,
        method="multi",
        chunksize=500
    )

    # 3. Prepare order_items dataframe
    item_cols = ["order_id", "sku_id", "sku_count"]
    items_df = raw_df[item_cols].drop_duplicates().copy()

    # 4. Insert into order_items
    items_df.to_sql(
        name="order_items",
        con=engine,
        if_exists="append",
        index=False,
        method="multi",
        chunksize=500
    )

    print(f"[SUCCESS] {len(fact_df)} orders and {len(items_df)} line items loaded.")


# -------------------------------------------------------------
# STEP 3: Orchestrator
# -------------------------------------------------------------
def run_table_based_load(customers_df: pd.DataFrame,
                         orders_raw_df: pd.DataFrame,
                         orders_order_level_df: pd.DataFrame):
    """
    Runs the full table-based loading sequence:
      1. Ensure tables exist
      2. Load customers
      3. Load orders (fact + items)
    """
    print("[START] Running table-based data load...")
    create_tables()
    load_customers(customers_df)
    load_orders(orders_order_level_df, orders_raw_df)
    print("[COMPLETE] Table-based load finished successfully.")
