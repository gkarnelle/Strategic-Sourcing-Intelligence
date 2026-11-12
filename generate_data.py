
"""Build connected sourcing data from GaiAnQi Global Trade V2."""

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent
SOURCE = (
    "https://raw.githubusercontent.com/"
    "gkarnelle/Global-Trade-Data-Analysis/main/v2/data/"
)

def load(filename):
    return pd.read_csv(SOURCE + filename)

suppliers = load("suppliers.csv")
orders = load("purchase_orders.csv")
lines = load("purchase_order_lines.csv")

# Validate canonical identifiers.
for name, frame, key in [
    ("suppliers", suppliers, "supplier_id"),
    ("purchase orders", orders, "purchase_order_id"),
    ("purchase order lines", lines, "purchase_order_line_id"),
]:
    if frame[key].isna().any() or frame[key].duplicated().any():
        raise ValueError(f"Invalid identifiers in {name}")

if not orders["supplier_id"].isin(suppliers["supplier_id"]).all():
    raise ValueError("Purchase orders reference unknown suppliers")

if not lines["purchase_order_id"].isin(
    orders["purchase_order_id"]
).all():
    raise ValueError("Purchase order lines reference unknown orders")

# Validate financial consistency.
line_totals = lines.groupby("purchase_order_id")[
    "line_value_usd"
].sum()

comparison = orders.set_index("purchase_order_id")[
    "total_order_value_usd"
].sub(line_totals, fill_value=0)

if (comparison.abs() > 0.01).any():
    raise ValueError("Purchase order and line totals do not reconcile")

# Create a sourcing transaction for each purchase order line.
transactions = lines.merge(
    orders[
        [
            "purchase_order_id",
            "supplier_id",
            "order_date",
            "purchase_order_status",
        ]
    ],
    on="purchase_order_id",
    validate="many_to_one",
)

transactions = transactions.rename(
    columns={
        "purchase_order_line_id": "transaction_id",
        "order_date": "transaction_date",
        "line_value_usd": "amount_usd",
    }
)

transactions = transactions[
    [
        "transaction_id",
        "purchase_order_id",
        "product_id",
        "supplier_id",
        "transaction_date",
        "purchase_order_status",
        "quantity_ordered",
        "unit_cost_usd",
        "amount_usd",
    ]
]

# Save only after successful validation.
suppliers.to_csv(ROOT / "suppliers.csv", index=False)
orders.to_csv(ROOT / "purchase_orders.csv", index=False)
transactions.to_csv(ROOT / "transactions.csv", index=False)

print("GaiAnQi sourcing integration complete")
print(f"Suppliers: {len(suppliers):,}")
print(f"Purchase orders: {len(orders):,}")
print(f"Procurement line transactions: {len(transactions):,}")
print(f"Purchase order value: ${orders['total_order_value_usd'].sum():,.2f}")
