# KanzPharma Desktop Suite

KanzPharma is a production-ready desktop application designed for managing a supplement-focused e-commerce business. It provides unified visibility across sales, inventory, logistics, marketing, and advanced analytics.

## Features
- **Multi-tab desktop GUI** with Sales, Inventory, Logistics, Marketing, Analytics, and Settings.
- **Role-based access** for Admin, Manager, Analyst, and Ops teams.
- **Real-time notifications** via backend API updates.
- **Analytics dashboards** with KPI cards, charts, and cohort analysis.
- **Exports** to CSV, Excel, and PDF formats.
- **PostgreSQL-ready data layer** with optional SQLite caching for offline use.
- **Logistics tracking** for shipments, carriers, and delivery status.

## Tech Stack
- **Desktop:** PyQt6
- **Backend:** FastAPI
- **Data Processing:** Pandas
- **Visualization:** Matplotlib (Plotly-compatible data outputs)
- **Database:** PostgreSQL + SQLite cache

## Installation
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Database Setup
1. Provision PostgreSQL and set the connection string:
   ```bash
   export KANZPHARMA_DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/kanzpharma
   ```
2. Initialize the tables and load sample data:
   ```bash
   python scripts/init_db.py
   ```
3. A local SQLite cache is created automatically when PostgreSQL is not configured.

## Running the Backend
```bash
uvicorn kanzpharma.backend.main:app --reload
```

## Running the Desktop App
```bash
python -m kanzpharma.desktop.main
```

## KPI Interpretation
- **Break-Even ROAS:** Minimum ROAS required to cover costs given gross margin.
- **Customer LTV:** Avg order value × purchase frequency × margin × retention window.
- **MER (Marketing Efficiency Ratio):** Revenue / marketing spend.
- **EBITDA:** Revenue minus COGS and operating expenses.
- **Cash Conversion Cycle:** DSO + DIO - DPO.

## Sample Dataset
Sample CSV files live in the `data/` directory and seed dashboards for:
- Customers
- Products
- Orders
- Inventory
- Marketing spend
- Logistics shipments

## Extensibility
The architecture provides hooks for:
- Shopify/WooCommerce order ingestion.
- Stripe and PayFast payment reconciliation.
- Email/SMS workflows via SendGrid/Twilio.
- Logistics carrier integrations for shipment tracking.
