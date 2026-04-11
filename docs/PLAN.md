# KanzPharma Delivery Plan

## 1. Product Vision
Deliver a production-ready desktop suite for KanzPharma that unifies Sales, Inventory, Logistics, Marketing, Analytics, and Settings in a single multi-user interface. The system will support role-based permissions, advanced KPI reporting, and modular integrations for future e-commerce growth.

## 2. Core Modules
1. **Sales**
   - Order lifecycle tracking, revenue aggregation, and discount analysis.
   - Customer segmentation insights and repeat-purchase monitoring.
2. **Inventory & Logistics**
   - Multi-warehouse stock visibility.
   - Reorder-point alerts and lead-time tracking.
3. **Marketing**
   - Campaign-level spend vs revenue analysis.
   - Attribution, ROAS, CTR, and CVR metrics.
4. **Analytics**
   - KPI dashboard: LTV, Break-Even ROAS, MER, EBITDA, and Cash Conversion Cycle.
   - Cohort analysis by acquisition month.
   - Export to CSV, Excel, and PDF.
5. **Settings & Security**
   - Role-based access control.
   - Theme toggle (light/dark).
   - Connection settings for backend and database.

## 3. Technical Architecture
- **Desktop GUI:** PyQt6 with multi-tab layout and embedded Matplotlib charts.
- **Backend API:** FastAPI for KPI computation, notifications, and data services.
- **Data Layer:** PostgreSQL as primary storage, SQLite cache for offline mode.
- **Data Processing:** Pandas for transformation, KPI computations, cohort analysis.
- **Reporting & Visualization:** Matplotlib and Plotly-compatible data structures.

## 4. Milestones
1. **Foundation (Week 1)**
   - Setup repo structure, dependencies, and sample data.
   - Define SQL schema for PostgreSQL.
2. **Core Functionality (Week 2-3)**
   - Implement backend KPI endpoints and dashboard data.
   - Build PyQt6 interface with Sales, Inventory, Marketing, Analytics, Settings tabs.
3. **Analytics & Reporting (Week 4)**
   - Implement KPI formulas (LTV, MER, EBITDA, CCC).
   - Export engine for CSV/Excel/PDF.
4. **Security & Scale (Week 5)**
   - Role-based permissions and user profiles.
   - Prepare integration hooks for payments, e-commerce platforms, and messaging.

## 5. Integration Roadmap
- E-commerce (Shopify, WooCommerce)
- Payment gateways (Stripe, PayFast)
- Communication (Twilio SMS, SendGrid email)
- Logistics partners for live fulfillment updates

## 6. Testing Strategy
- KPI validation with known test data.
- UI smoke tests for navigation and export.
- API endpoint checks (health, KPIs, dashboard).

## 7. Documentation Outputs
- Installation and setup guide.
- KPI interpretation reference.
- Database setup instructions for PostgreSQL.
- Sample dataset usage notes.
