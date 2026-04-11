from __future__ import annotations

import pandas as pd


def calculate_break_even_roas(gross_margin: float) -> float:
    return 1 / gross_margin if gross_margin else 0.0


def calculate_ltv(avg_order_value: float, purchase_frequency: float, gross_margin: float, retention_months: int) -> float:
    return avg_order_value * purchase_frequency * gross_margin * retention_months


def calculate_mer(total_revenue: float, total_marketing_spend: float) -> float:
    return total_revenue / total_marketing_spend if total_marketing_spend else 0.0


def calculate_ebitda(revenue: float, cogs: float, opex: float) -> float:
    return revenue - cogs - opex


def calculate_cash_conversion_cycle(dso: float, dio: float, dpo: float) -> float:
    return dso + dio - dpo


def compute_sales_summary(orders: pd.DataFrame, products: pd.DataFrame) -> pd.DataFrame:
    merged = orders.merge(products, on="product_id", how="left")
    merged["gross_revenue"] = merged["retail_price"] * merged["quantity"]
    merged["discount_value"] = merged["gross_revenue"] * merged["discount"]
    merged["net_revenue"] = merged["gross_revenue"] - merged["discount_value"]
    merged["cogs"] = merged["cost_price"] * merged["quantity"]
    return merged


def compute_marketing_metrics(marketing: pd.DataFrame) -> pd.DataFrame:
    marketing = marketing.copy()
    marketing["ctr"] = (marketing["clicks"] / marketing["impressions"]).fillna(0.0)
    marketing["cvr"] = (marketing["conversions"] / marketing["clicks"]).fillna(0.0)
    marketing["roas"] = (marketing["attributed_revenue"] / marketing["spend"]).fillna(0.0)
    return marketing
