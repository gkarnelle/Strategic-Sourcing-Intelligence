
"""Analyze connected GaiAnQi procurement data and build executive dashboard."""

from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

suppliers = pd.read_csv(ROOT / "suppliers.csv")
orders = pd.read_csv(ROOT / "purchase_orders.csv")
tx = pd.read_csv(ROOT / "transactions.csv", parse_dates=["transaction_date"])

required = {
    "transaction_id", "purchase_order_id", "product_id",
    "supplier_id", "transaction_date", "amount_usd"
}
missing = required - set(tx.columns)
if missing:
    raise ValueError(f"Missing transaction columns: {missing}")

for frame, key in [
    (suppliers, "supplier_id"),
    (orders, "purchase_order_id"),
    (tx, "transaction_id"),
]:
    if frame[key].isna().any() or frame[key].duplicated().any():
        raise ValueError(f"Invalid or duplicate {key}")

if tx["amount_usd"].isna().any() or (tx["amount_usd"] <= 0).any():
    raise ValueError("Missing or nonpositive transaction values")

if not tx["supplier_id"].isin(suppliers["supplier_id"]).all():
    raise ValueError("Unknown supplier IDs")

if not tx["purchase_order_id"].isin(orders["purchase_order_id"]).all():
    raise ValueError("Unknown purchase order IDs")

# Validate that each transaction matches its purchase order supplier.
check = tx.merge(
    orders[["purchase_order_id", "supplier_id"]],
    on="purchase_order_id",
    suffixes=("", "_order"),
    validate="many_to_one",
)
if (check["supplier_id"] != check["supplier_id_order"]).any():
    raise ValueError("Supplier mismatch between transactions and orders")

# Reconcile PO totals.
totals = tx.groupby("purchase_order_id")["amount_usd"].sum()
difference = orders.set_index("purchase_order_id")[
    "total_order_value_usd"
].sub(totals, fill_value=0)

if (difference.abs() > 0.01).any():
    raise ValueError("Procurement line values do not reconcile to PO totals")

df = tx.merge(suppliers, on="supplier_id", validate="many_to_one")
df["year"] = df["transaction_date"].dt.year

total_spend = df["amount_usd"].sum()
supplier_count = df["supplier_id"].nunique()
po_count = orders["purchase_order_id"].nunique()
product_count = df["product_id"].nunique()

# SUPPLIER INTELLIGENCE
spend = (
    df.groupby(["supplier_id", "supplier_name"], as_index=False)
    .agg(
        spend_usd=("amount_usd", "sum"),
        purchase_order_count=("purchase_order_id", "nunique"),
        product_count=("product_id", "nunique"),
    )
    .sort_values("spend_usd", ascending=False)
    .reset_index(drop=True)
)
spend["share_pct"] = spend["spend_usd"] / total_spend * 100
spend["cumulative_share_pct"] = spend["share_pct"].cumsum()
spend.to_csv(OUT / "supplier_spend.csv", index=False)

concentration = spend.loc[spend["share_pct"] > 10].copy()
concentration.to_csv(OUT / "concentration_flags.csv", index=False)

top_10_share = spend.head(10)["share_pct"].sum()
top_5_share = spend.head(5)["share_pct"].sum()

# PRODUCT INTELLIGENCE
products = (
    df.groupby("product_id", as_index=False)
    .agg(
        spend_usd=("amount_usd", "sum"),
        supplier_count=("supplier_id", "nunique"),
        purchase_order_count=("purchase_order_id", "nunique"),
        quantity_ordered=("quantity_ordered", "sum"),
    )
    .sort_values("spend_usd", ascending=False)
)
products.to_csv(OUT / "product_spend.csv", index=False)

# COUNTRY EXPOSURE
country = (
    df.groupby("country", as_index=False)["amount_usd"]
    .sum()
    .rename(columns={"amount_usd": "spend_usd"})
    .sort_values("spend_usd", ascending=False)
)
country["share_pct"] = country["spend_usd"] / total_spend * 100
country.to_csv(OUT / "country_spend.csv", index=False)

# ANNUAL PROCUREMENT TRENDS
annual = (
    df.groupby("year", as_index=False)
    .agg(
        spend_usd=("amount_usd", "sum"),
        purchase_order_count=("purchase_order_id", "nunique"),
        supplier_count=("supplier_id", "nunique"),
    )
    .sort_values("year")
)
annual.to_csv(OUT / "annual_spend.csv", index=False)

# ILLUSTRATIVE SOURCING OPPORTUNITIES
# These are prioritization scenarios, not realized savings.
# No contract coverage is assumed because contract data is unavailable.
opportunities = products.head(10).copy()
opportunities["illustrative_addressable_pct"] = 0.25
opportunities["illustrative_savings_rate"] = 0.03
opportunities["illustrative_savings_usd"] = (
    opportunities["spend_usd"]
    * opportunities["illustrative_addressable_pct"]
    * opportunities["illustrative_savings_rate"]
).round(2)
opportunities["priority_rank"] = range(1, len(opportunities) + 1)
opportunities.to_csv(OUT / "sourcing_opportunities.csv", index=False)

scenarios = {
    "Conservative": (0.10, 0.02),
    "Moderate": (0.25, 0.03),
    "Ambitious": (0.40, 0.05),
}

scenario_rows = []
for name, (addressable, rate) in scenarios.items():
    savings = total_spend * addressable * rate
    scenario_rows.append({
        "scenario": name,
        "addressable_pct": addressable * 100,
        "savings_rate_pct": rate * 100,
        "estimated_savings_usd": round(savings, 2),
        "savings_pct_total_spend": round(savings / total_spend * 100, 2),
    })

savings_df = pd.DataFrame(scenario_rows)
savings_df.to_csv(OUT / "savings_scenarios.csv", index=False)

summary = pd.DataFrame([{
    "total_po_value_usd": round(total_spend, 2),
    "active_suppliers": supplier_count,
    "purchase_orders": po_count,
    "procurement_lines": len(df),
    "products_purchased": product_count,
    "top_5_supplier_spend_pct": round(top_5_share, 2),
    "top_10_supplier_spend_pct": round(top_10_share, 2),
    "supplier_concentration_flags": len(concentration),
    "countries_sourced_from": df["country"].nunique(),
    "illustrative_moderate_savings_usd": savings_df.loc[
        savings_df["scenario"] == "Moderate",
        "estimated_savings_usd"
    ].iloc[0],
}])
summary.to_csv(OUT / "executive_summary.csv", index=False)

# DYNAMIC EXECUTIVE RECOMMENDATIONS
recommendations = [
    {
        "priority": 1,
        "recommendation": (
            f"Review sourcing exposure to {spend.iloc[0]['supplier_name']} "
            f"({spend.iloc[0]['share_pct']:.1f}% of PO value)."
        ),
    },
    {
        "priority": 2,
        "recommendation": (
            f"Evaluate purchasing strategy for {products.iloc[0]['product_id']}, "
            "the highest-value product."
        ),
    },
    {
        "priority": 3,
        "recommendation": (
            f"Monitor country exposure to {country.iloc[0]['country']} "
            f"({country.iloc[0]['share_pct']:.1f}% of PO value)."
        ),
    },
]
pd.DataFrame(recommendations).to_csv(
    OUT / "executive_recommendations.csv", index=False
)

# EXECUTIVE DASHBOARD
NAVY = "#17324D"
TEAL = "#197F8C"
GOLD = "#D99A36"
GRAY = "#66788A"
BG = "#F5F7FA"

fig = plt.figure(figsize=(16, 12), facecolor=BG)

fig.text(
    .06, .96, "GAIANQI | STRATEGIC SOURCING INTELLIGENCE",
    fontsize=20, fontweight="bold", color=NAVY
)
fig.text(
    .06, .932,
    "Connected Procurement Analytics | Synthetic Data | 2022-2026",
    fontsize=11, color=GRAY
)

def money(value):
    if abs(value) >= 1e6:
        return f"${value / 1e6:,.2f}M"
    return f"${value / 1e3:,.1f}K"

kpis = [
    ("PURCHASE ORDER VALUE", money(total_spend)),
    ("ACTIVE SUPPLIERS", f"{supplier_count:,}"),
    ("PURCHASE ORDERS", f"{po_count:,}"),
    ("TOP 10 SUPPLIER SHARE", f"{top_10_share:.1f}%"),
]

for i, (label, value) in enumerate(kpis):
    x = .06 + i * .235
    ax = fig.add_axes([x, .81, .215, .095])
    ax.set_facecolor("white")
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.text(
        .05, .70, label, transform=ax.transAxes,
        fontsize=9, color=GRAY, fontweight="bold"
    )
    ax.text(
        .05, .17, value, transform=ax.transAxes,
        fontsize=22, color=TEAL, fontweight="bold"
    )

# Supplier concentration
ax1 = fig.add_axes([.09, .49, .37, .25])
top_suppliers = spend.head(7).iloc[::-1]
ax1.barh(
    top_suppliers["supplier_id"],
    top_suppliers["spend_usd"],
    color=TEAL
)
ax1.set_title(
    "01 | Top Suppliers by PO Value",
    loc="left", fontweight="bold", color=NAVY, pad=14
)
ax1.xaxis.set_major_formatter(
    FuncFormatter(lambda x, pos: money(x))
)
ax1.spines[["top", "right"]].set_visible(False)

# Annual spend
ax2 = fig.add_axes([.57, .49, .36, .25])
ax2.bar(
    annual["year"].astype(str),
    annual["spend_usd"],
    color=GOLD
)
ax2.set_title(
    "02 | Annual Purchase Order Value",
    loc="left", fontweight="bold", color=NAVY, pad=14
)
ax2.yaxis.set_major_formatter(
    FuncFormatter(lambda x, pos: money(x))
)
ax2.spines[["top", "right"]].set_visible(False)

# Country exposure
ax3 = fig.add_axes([.09, .19, .37, .22])
country_top = country.head(6).iloc[::-1]
ax3.barh(
    country_top["country"],
    country_top["spend_usd"],
    color=TEAL
)
ax3.set_title(
    "03 | Procurement by Supplier Country",
    loc="left", fontweight="bold", color=NAVY, pad=14
)
ax3.xaxis.set_major_formatter(
    FuncFormatter(lambda x, pos: money(x))
)
ax3.spines[["top", "right"]].set_visible(False)

# Savings scenarios
ax4 = fig.add_axes([.57, .19, .36, .22])
ax4.bar(
    savings_df["scenario"],
    savings_df["estimated_savings_usd"],
    color=["#A6C5CA", TEAL, GOLD]
)
ax4.set_title(
    "04 | Hypothetical Savings Scenarios",
    loc="left", fontweight="bold", color=NAVY, pad=14
)
ax4.yaxis.set_major_formatter(
    FuncFormatter(lambda x, pos: money(x))
)
ax4.spines[["top", "right"]].set_visible(False)

# Executive recommendations
fig.text(
    .06, .125, "05 | EXECUTIVE PRIORITIES",
    fontsize=12, fontweight="bold", color=NAVY
)

for i, item in enumerate(recommendations):
    fig.text(
        .07, .103 - i * .022,
        f"{item['priority']:02d}  {item['recommendation']}",
        fontsize=10, color=NAVY
    )

fig.text(
    .06, .018,
    "Synthetic procurement data. PO value is not paid spend. "
    "Savings are illustrative assumptions, not realized results.",
    fontsize=9, color=GRAY
)

fig.savefig(
    OUT / "sourcing_dashboard.png",
    dpi=180, bbox_inches="tight",
    facecolor=BG
)
plt.close(fig)

print("\nGAIANQI STRATEGIC SOURCING V2")
print(summary.to_string(index=False))
print("\nExecutive reports and dashboard saved in outputs/")
