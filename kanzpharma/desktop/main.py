from __future__ import annotations

import importlib
import importlib.util
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List

import requests
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QDialog,
    QFileDialog,
    QFormLayout,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
BACKEND_URL = "http://127.0.0.1:8000"


@dataclass
class UserProfile:
    name: str
    role: str


ROLE_PERMISSIONS = {
    "Admin": {"sales", "inventory", "logistics", "marketing", "analytics", "settings"},
    "Manager": {"sales", "inventory", "logistics", "marketing", "analytics"},
    "Analyst": {"analytics", "marketing"},
    "Ops": {"sales", "inventory", "logistics"},
}


class LoginDialog(QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("KanzPharma Login")
        self.name_input = QLineEdit()
        self.role_selector = QComboBox()
        self.role_selector.addItems(list(ROLE_PERMISSIONS.keys()))
        self.submit_button = QPushButton("Sign In")
        self.submit_button.clicked.connect(self.accept)

        layout = QFormLayout()
        layout.addRow("Name", self.name_input)
        layout.addRow("Role", self.role_selector)
        layout.addRow(self.submit_button)
        self.setLayout(layout)

    def user_profile(self) -> UserProfile:
        return UserProfile(
            name=self.name_input.text() or "Guest",
            role=self.role_selector.currentText(),
        )


class MetricCard(QGroupBox):
    def __init__(self, title: str) -> None:
        super().__init__()
        self.setTitle(title)
        self.value_label = QLabel("--")
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout = QVBoxLayout()
        layout.addWidget(self.value_label)
        self.setLayout(layout)

    def update_value(self, value: str) -> None:
        self.value_label.setText(value)


class ChartWidget(QWidget):
    def __init__(self, title: str) -> None:
        super().__init__()
        self.figure = Figure(figsize=(5, 3))
        self.canvas = FigureCanvas(self.figure)
        self.title_label = QLabel(title)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def plot_bar(self, labels: List[str], values: List[float]) -> None:
        self.figure.clear()
        axis = self.figure.add_subplot(111)
        axis.bar(labels, values, color="#5B8FF9")
        axis.set_ylabel("Revenue")
        axis.tick_params(axis="x", rotation=30)
        self.figure.tight_layout()
        self.canvas.draw()


class KanzPharmaApp(QMainWindow):
    def __init__(self, user: UserProfile) -> None:
        super().__init__()
        self.user = user
        self.setWindowTitle("KanzPharma Desktop Suite")
        self.resize(1200, 800)
        self.dependencies_ok = self.check_dependencies()

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.dashboard_tab = QWidget()
        self.sales_tab = QWidget()
        self.inventory_tab = QWidget()
        self.logistics_tab = QWidget()
        self.marketing_tab = QWidget()
        self.analytics_tab = QWidget()
        self.settings_tab = QWidget()

        self.tabs_map = {
            "sales": self.sales_tab,
            "inventory": self.inventory_tab,
            "logistics": self.logistics_tab,
            "marketing": self.marketing_tab,
            "analytics": self.analytics_tab,
            "settings": self.settings_tab,
        }

        self.build_toolbar()
        self.build_dashboard()
        self.build_sales()
        self.build_inventory()
        self.build_logistics()
        self.build_marketing()
        self.build_analytics()
        self.build_settings()

        self.tabs.addTab(self.dashboard_tab, "Dashboard")
        self.tabs.addTab(self.sales_tab, "Sales")
        self.tabs.addTab(self.inventory_tab, "Inventory")
        self.tabs.addTab(self.logistics_tab, "Logistics")
        self.tabs.addTab(self.marketing_tab, "Marketing")
        self.tabs.addTab(self.analytics_tab, "Analytics")
        self.tabs.addTab(self.settings_tab, "Settings")

        self.apply_permissions()
        self.init_notifications()
        if self.dependencies_ok:
            self.refresh_data()
        else:
            QMessageBox.warning(
                self,
                "Missing Dependencies",
                "Required packages are missing. Please install dependencies from requirements.txt.",
            )

    def check_dependencies(self) -> bool:
        required = ["pandas"]
        missing = [name for name in required if importlib.util.find_spec(name) is None]
        return not missing

    def load_pandas(self):
        return importlib.import_module("pandas")

    def build_toolbar(self) -> None:
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)

        refresh_action = QAction("Refresh", self)
        refresh_action.triggered.connect(self.refresh_data)
        toolbar.addAction(refresh_action)

        export_action = QAction("Export Report", self)
        export_action.triggered.connect(self.export_reports)
        toolbar.addAction(export_action)

        self.theme_action = QAction("Toggle Dark Mode", self)
        self.theme_action.triggered.connect(self.toggle_theme)
        toolbar.addAction(self.theme_action)

    def build_dashboard(self) -> None:
        layout = QVBoxLayout()
        card_layout = QGridLayout()

        self.kpi_cards = {
            "break_even_roas": MetricCard("Break-Even ROAS"),
            "ltv": MetricCard("Customer LTV"),
            "mer": MetricCard("MER"),
            "ebitda": MetricCard("EBITDA"),
            "ccc": MetricCard("Cash Conversion Cycle"),
        }

        for index, card in enumerate(self.kpi_cards.values()):
            card_layout.addWidget(card, 0, index)

        chart_layout = QHBoxLayout()
        self.revenue_chart = ChartWidget("Revenue by Channel")
        self.product_chart = ChartWidget("Top Products")
        chart_layout.addWidget(self.revenue_chart)
        chart_layout.addWidget(self.product_chart)

        self.notifications_list = QListWidget()
        notifications_group = QGroupBox("Real-Time Notifications")
        notifications_layout = QVBoxLayout()
        notifications_layout.addWidget(self.notifications_list)
        notifications_group.setLayout(notifications_layout)

        layout.addLayout(card_layout)
        layout.addLayout(chart_layout)
        layout.addWidget(notifications_group)
        self.dashboard_tab.setLayout(layout)

    def build_sales(self) -> None:
        layout = QVBoxLayout()
        self.sales_table = QTableWidget()
        layout.addWidget(QLabel("Orders Overview"))
        layout.addWidget(self.sales_table)
        self.sales_tab.setLayout(layout)

    def build_inventory(self) -> None:
        layout = QVBoxLayout()
        self.inventory_table = QTableWidget()
        layout.addWidget(QLabel("Inventory & Reorder Points"))
        layout.addWidget(self.inventory_table)
        self.inventory_tab.setLayout(layout)

    def build_logistics(self) -> None:
        layout = QVBoxLayout()
        self.logistics_table = QTableWidget()
        layout.addWidget(QLabel("Shipment & Fulfillment Tracking"))
        layout.addWidget(self.logistics_table)
        self.logistics_tab.setLayout(layout)

    def build_marketing(self) -> None:
        layout = QVBoxLayout()
        self.marketing_table = QTableWidget()
        self.marketing_metrics_table = QTableWidget()
        layout.addWidget(QLabel("Campaign Performance"))
        layout.addWidget(self.marketing_table)
        layout.addWidget(QLabel("Attribution & Conversion Metrics"))
        layout.addWidget(self.marketing_metrics_table)
        self.marketing_tab.setLayout(layout)

    def build_analytics(self) -> None:
        layout = QVBoxLayout()
        self.cohort_table = QTableWidget()
        self.cohort_table.setColumnCount(4)
        self.cohort_table.setHorizontalHeaderLabels([
            "Cohort Month",
            "Customers",
            "Repeat Rate",
            "Revenue",
        ])
        layout.addWidget(QLabel("Cohort Analysis"))
        layout.addWidget(self.cohort_table)
        self.analytics_tab.setLayout(layout)

    def build_settings(self) -> None:
        layout = QFormLayout()
        self.user_label = QLabel(f"Signed in as {self.user.name} ({self.user.role})")
        self.backend_input = QLineEdit(BACKEND_URL)
        self.cache_toggle = QComboBox()
        self.cache_toggle.addItems(["SQLite Cache", "PostgreSQL Primary"])
        layout.addRow("User", self.user_label)
        layout.addRow("Backend URL", self.backend_input)
        layout.addRow("Storage Mode", self.cache_toggle)
        self.settings_tab.setLayout(layout)

    def apply_permissions(self) -> None:
        allowed = ROLE_PERMISSIONS.get(self.user.role, set())
        for key, tab in self.tabs_map.items():
            index = self.tabs.indexOf(tab)
            if index >= 0:
                self.tabs.setTabEnabled(index, key in allowed)

    def init_notifications(self) -> None:
        self.notification_timer = QTimer(self)
        self.notification_timer.timeout.connect(self.refresh_notifications)
        self.notification_timer.start(15000)

    def refresh_data(self) -> None:
        if not self.dependencies_ok:
            return
        self.refresh_kpis()
        self.refresh_dashboard_charts()
        self.load_table(self.sales_table, DATA_DIR / "orders.csv")
        self.load_table(self.inventory_table, DATA_DIR / "inventory.csv")
        self.load_table(self.logistics_table, DATA_DIR / "logistics.csv")
        self.load_table(self.marketing_table, DATA_DIR / "marketing_spend.csv")
        self.refresh_marketing_metrics()
        self.populate_cohort_analysis()
        self.refresh_notifications()

    def refresh_kpis(self) -> None:
        try:
            response = requests.get(f"{self.backend_input.text()}/kpis", timeout=5)
            response.raise_for_status()
            data = response.json()
        except (requests.RequestException, json.JSONDecodeError):
            data = {}

        self.kpi_cards["break_even_roas"].update_value(f"{data.get('break_even_roas', 0):.2f}x")
        self.kpi_cards["ltv"].update_value(f"${data.get('ltv', 0):,.2f}")
        self.kpi_cards["mer"].update_value(f"{data.get('mer', 0):.2f}x")
        self.kpi_cards["ebitda"].update_value(f"${data.get('ebitda', 0):,.2f}")
        self.kpi_cards["ccc"].update_value(f"{data.get('cash_conversion_cycle', 0):.1f} days")

    def refresh_dashboard_charts(self) -> None:
        try:
            response = requests.get(f"{self.backend_input.text()}/dashboard", timeout=5)
            response.raise_for_status()
            dashboard_data = response.json()
        except (requests.RequestException, json.JSONDecodeError):
            dashboard_data = {"revenue_by_channel": [], "top_products": []}

        revenue_data = dashboard_data.get("revenue_by_channel", [])
        self.revenue_chart.plot_bar(
            [row["channel"] for row in revenue_data],
            [row["net_revenue"] for row in revenue_data],
        )

        product_data = dashboard_data.get("top_products", [])
        self.product_chart.plot_bar(
            [row["product_id"] for row in product_data],
            [row["net_revenue"] for row in product_data],
        )

    def refresh_marketing_metrics(self) -> None:
        pd = self.load_pandas()
        try:
            response = requests.get(f"{self.backend_input.text()}/marketing", timeout=5)
            response.raise_for_status()
            marketing_data = response.json().get("marketing", [])
            df = pd.DataFrame(marketing_data)
        except (requests.RequestException, json.JSONDecodeError, ValueError):
            df = pd.read_csv(DATA_DIR / "marketing_spend.csv")
            df["ctr"] = (df["clicks"] / df["impressions"]).fillna(0.0)
            df["cvr"] = (df["conversions"] / df["clicks"]).fillna(0.0)
            df["roas"] = (df["attributed_revenue"] / df["spend"]).fillna(0.0)

        columns = [
            "campaign_id",
            "channel",
            "month",
            "spend",
            "attributed_revenue",
            "ctr",
            "cvr",
            "roas",
        ]
        df = df[columns]
        self.marketing_metrics_table.setRowCount(len(df))
        self.marketing_metrics_table.setColumnCount(len(columns))
        self.marketing_metrics_table.setHorizontalHeaderLabels(columns)
        for row_idx, (_, row) in enumerate(df.iterrows()):
            for col_idx, value in enumerate(row):
                self.marketing_metrics_table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
        self.marketing_metrics_table.resizeColumnsToContents()

    def refresh_notifications(self) -> None:
        self.notifications_list.clear()
        try:
            response = requests.get(f"{self.backend_input.text()}/notifications", timeout=5)
            response.raise_for_status()
            notifications = response.json()
        except (requests.RequestException, json.JSONDecodeError):
            notifications = []

        for notice in notifications:
            item = QListWidgetItem(f"{notice['title']}: {notice['message']}")
            if notice["severity"] == "warning":
                item.setForeground(Qt.GlobalColor.darkYellow)
            elif notice["severity"] == "info":
                item.setForeground(Qt.GlobalColor.darkBlue)
            self.notifications_list.addItem(item)

    def load_table(self, table: QTableWidget, file_path: Path) -> None:
        pd = self.load_pandas()
        df = pd.read_csv(file_path)
        table.setRowCount(len(df))
        table.setColumnCount(len(df.columns))
        table.setHorizontalHeaderLabels(df.columns)
        for row_idx, (_, row) in enumerate(df.iterrows()):
            for col_idx, value in enumerate(row):
                table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
        table.resizeColumnsToContents()

    def populate_cohort_analysis(self) -> None:
        pd = self.load_pandas()
        orders = pd.read_csv(DATA_DIR / "orders.csv", parse_dates=["order_date"])
        customers = pd.read_csv(DATA_DIR / "customers.csv", parse_dates=["signup_date"])
        products = pd.read_csv(DATA_DIR / "products.csv")
        merged = orders.merge(customers, on="customer_id", how="left").merge(products, on="product_id", how="left")
        merged["gross_revenue"] = merged["retail_price"] * merged["quantity"]
        merged["discount_value"] = merged["gross_revenue"] * merged["discount"]
        merged["net_revenue"] = merged["gross_revenue"] - merged["discount_value"]
        merged["cohort_month"] = merged["signup_date"].dt.to_period("M").astype(str)
        cohort_summary = (
            merged.groupby("cohort_month").agg(
                customers=("customer_id", "nunique"),
                revenue=("net_revenue", "sum"),
            )
        )
        cohort_summary["repeat_rate"] = (merged.groupby("cohort_month")["customer_id"].count() / cohort_summary["customers"]).values
        cohort_summary = cohort_summary.reset_index()

        self.cohort_table.setRowCount(len(cohort_summary))
        for row_idx, row in cohort_summary.iterrows():
            self.cohort_table.setItem(row_idx, 0, QTableWidgetItem(row["cohort_month"]))
            self.cohort_table.setItem(row_idx, 1, QTableWidgetItem(str(int(row["customers"]))))
            self.cohort_table.setItem(row_idx, 2, QTableWidgetItem(f"{row['repeat_rate']:.2f}"))
            self.cohort_table.setItem(row_idx, 3, QTableWidgetItem(str(int(row["revenue"]))))
        self.cohort_table.resizeColumnsToContents()

    def export_reports(self) -> None:
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Report",
            "kanzpharma_report",
            "CSV Files (*.csv);;Excel Files (*.xlsx);;PDF Files (*.pdf)",
        )
        if not file_path:
            return

        pd = self.load_pandas()
        sales_df = pd.read_csv(DATA_DIR / "orders.csv")
        if file_path.endswith(".csv"):
            sales_df.to_csv(file_path, index=False)
        elif file_path.endswith(".xlsx"):
            sales_df.to_excel(file_path, index=False)
        elif file_path.endswith(".pdf"):
            figure = Figure()
            axis = figure.add_subplot(111)
            axis.axis("off")
            axis.table(cellText=sales_df.values, colLabels=sales_df.columns, loc="center")
            figure.savefig(file_path, bbox_inches="tight")

        QMessageBox.information(self, "Export Complete", "Report exported successfully.")

    def toggle_theme(self) -> None:
        if self.styleSheet():
            self.setStyleSheet("")
        else:
            self.setStyleSheet(
                "QWidget { background-color: #1f1f1f; color: #f5f5f5; }"
                "QTableWidget { background-color: #2a2a2a; gridline-color: #444; }"
                "QHeaderView::section { background-color: #333; color: #fff; }"
            )


def main() -> None:
    app = QApplication(sys.argv)
    login = LoginDialog()
    if login.exec() != QDialog.DialogCode.Accepted:
        sys.exit()

    window = KanzPharmaApp(login.user_profile())
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
