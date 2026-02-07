from __future__ import annotations

import pathlib

import pandas as pd
from sqlalchemy import text

from kanzpharma.backend.db import engine
from kanzpharma.backend.models import Base

BASE_DIR = pathlib.Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"


def load_table(name: str, file_name: str) -> None:
    df = pd.read_csv(DATA_DIR / file_name)
    df.to_sql(name, engine, if_exists="replace", index=False)


def main() -> None:
    Base.metadata.create_all(bind=engine)
    load_table("customers", "customers.csv")
    load_table("products", "products.csv")
    load_table("orders", "orders.csv")
    load_table("inventory", "inventory.csv")
    load_table("marketing_spend", "marketing_spend.csv")
    load_table("logistics", "logistics.csv")

    with engine.begin() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM orders"))
        print("Orders loaded:", result.scalar())


if __name__ == "__main__":
    main()
