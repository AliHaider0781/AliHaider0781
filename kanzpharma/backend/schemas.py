from __future__ import annotations

from typing import List
from pydantic import BaseModel


class KPIResponse(BaseModel):
    break_even_roas: float
    ltv: float
    mer: float
    ebitda: float
    cash_conversion_cycle: float


class Notification(BaseModel):
    title: str
    message: str
    severity: str


class DashboardResponse(BaseModel):
    revenue_by_channel: List[dict]
    top_products: List[dict]
    inventory_alerts: List[dict]
