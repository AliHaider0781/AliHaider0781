from __future__ import annotations

import pathlib
from typing import Generator

import pandas as pd
from fastapi import FastAPI

from kanzpharma.backend.analytics import (
    calculate_break_even_roas,
    calculate_cash_conversion_cycle,
    calculate_ebitda,
    calculate_ltv,
    calculate_mer,
    compute_marketing_metrics,
    compute_sales_summary,
)
from kanzpharma.backend.schemas import DashboardResponse, KPIResponse, Notification

BASE_DIR = pathlib.Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"

app = FastAPI(title="KanzPharma Backend", version="1.0.0")


def load_data() -> dict:
    return {
        "customers": pd.read_csv(DATA_DIR / "customers.csv", parse_dates=["signup_date"]),
        "products": pd.read_csv(DATA_DIR / "products.csv"),
        "orders": pd.read_csv(DATA_DIR / "orders.csv", parse_dates=["order_date"]),
        "inventory": pd.read_csv(DATA_DIR / "inventory.csv"),
        "marketing": pd.read_csv(DATA_DIR / "marketing_spend.csv", parse_dates=["month"]),
        "logistics": pd.read_csv(DATA_DIR / "logistics.csv", parse_dates=["ship_date", "delivery_date"]),
    }


data_cache = load_data()


def get_sales_summary() -> pd.DataFrame:
    return compute_sales_summary(data_cache["orders"], data_cache["products"])


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/kpis", response_model=KPIResponse)
def kpis() -> KPIResponse:
    sales = get_sales_summary()
    revenue = float(sales["net_revenue"].sum())
    cogs = float(sales["cogs"].sum())
    gross_margin = (revenue - cogs) / revenue if revenue else 0.0
    avg_order_value = float(sales["net_revenue"].mean())
    purchase_frequency = 1.6
    retention_months = 18
    marketing_spend = float(data_cache["marketing"]["spend"].sum())
    opex = revenue * 0.22

    return KPIResponse(
        break_even_roas=calculate_break_even_roas(gross_margin),
        ltv=calculate_ltv(avg_order_value, purchase_frequency, gross_margin, retention_months),
        mer=calculate_mer(revenue, marketing_spend),
        ebitda=calculate_ebitda(revenue, cogs, opex),
        cash_conversion_cycle=calculate_cash_conversion_cycle(dso=28, dio=45, dpo=30),
    )


@app.get("/dashboard", response_model=DashboardResponse)
def dashboard() -> DashboardResponse:
    sales = get_sales_summary()
    revenue_by_channel = (
        sales.groupby("channel")["net_revenue"].sum().reset_index().sort_values("net_revenue", ascending=False)
    )
    top_products = (
        sales.groupby("product_id")["net_revenue"].sum().reset_index().sort_values("net_revenue", ascending=False)
    )
    inventory_alerts = data_cache["inventory"].query("on_hand <= reorder_point")

    return DashboardResponse(
        revenue_by_channel=revenue_by_channel.to_dict(orient="records"),
        top_products=top_products.to_dict(orient="records"),
        inventory_alerts=inventory_alerts.to_dict(orient="records"),
    )


@app.get("/marketing")
def marketing() -> dict:
    metrics = compute_marketing_metrics(data_cache["marketing"])
    return {"marketing": metrics.to_dict(orient="records")}


@app.get("/logistics")
def logistics() -> dict:
    return {"logistics": data_cache["logistics"].to_dict(orient="records")}


@app.get("/notifications", response_model=list[Notification])
def notifications() -> list[Notification]:
    return [
        Notification(
            title="Low Stock Alert",
            message="Magnesium Glycinate at Lahore warehouse below reorder point.",
            severity="warning",
        ),
        Notification(
            title="Campaign Spike",
            message="Instagram February ROAS increased 6% week-over-week.",
            severity="info",
        ),
    ]
