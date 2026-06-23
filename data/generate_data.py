import pandas as pd
import numpy as np
import sqlite3
import os

np.random.seed(42)

CATEGORIES = ["Electronics", "Clothing", "Food & Beverage", "Home & Garden", "Sports"]
PRODUCTS = {
    "Electronics": ["Laptop", "Smartphone", "Headphones", "Tablet", "Monitor"],
    "Clothing": ["T-Shirt", "Jeans", "Jacket", "Sneakers", "Dress"],
    "Food & Beverage": ["Coffee Beans", "Protein Bar", "Green Tea", "Energy Drink", "Smoothie"],
    "Home & Garden": ["Plant Pot", "LED Lamp", "Pillow Set", "Wall Clock", "Rug"],
    "Sports": ["Yoga Mat", "Dumbbells", "Running Shoes", "Water Bottle", "Jump Rope"],
}
REGIONS = ["North", "South", "East", "West", "Central"]
CHANNELS = ["Online", "In-Store", "Mobile App"]

N = 5000
dates = pd.date_range(start="2023-01-01", end="2024-12-31", periods=N)
categories = np.random.choice(CATEGORIES, N)
products = [np.random.choice(PRODUCTS[c]) for c in categories]

base_prices = {
    "Electronics": 500, "Clothing": 60, "Food & Beverage": 15,
    "Home & Garden": 45, "Sports": 35,
}
prices = np.array([int(base_prices[c] * np.random.uniform(0.7, 1.5)) for c in categories])
quantities = np.random.randint(1, 6, N).astype(int)
revenue = (prices * quantities).astype(int)
costs = (revenue * np.random.uniform(0.4, 0.65, N)).astype(int)
profit = (revenue - costs).astype(int)

df = pd.DataFrame({
    "order_id": range(1, N + 1),
    "date": dates.strftime("%Y-%m-%d"),
    "year": dates.year.astype(int),
    "month_num": dates.month.astype(int),
    "month_name": dates.strftime("%b %Y"),
    "category": categories,
    "product": products,
    "region": np.random.choice(REGIONS, N),
    "channel": np.random.choice(CHANNELS, N, p=[0.5, 0.3, 0.2]),
    "quantity": quantities,
    "unit_price": prices,
    "revenue": revenue,
    "cost": costs,
    "profit": profit,
})

csv_path = os.path.join(os.path.dirname(__file__), "sales.csv")
df.to_csv(csv_path, index=False, float_format="%.0f")
print(f"Generated {N} rows -> {csv_path}")

db_path = os.path.join(os.path.dirname(__file__), "sales.db")
conn = sqlite3.connect(db_path)
df.to_sql("sales", conn, if_exists="replace", index=False)
conn.close()
print(f"Loaded into SQLite -> {db_path}")

print("\nPreview:")
print(df[["date", "category", "revenue", "cost", "profit"]].head(3).to_string(index=False))
print(f"\nTotal revenue: {revenue.sum():,}")
print(f"Total profit:  {profit.sum():,}")
print(f"Total orders:  {N:,}")
