from dataclasses import dataclass


@dataclass(frozen=True)
class ProductMetrics:
    """Métricas operativas del SKU (entrada al evaluador de proposiciones)."""

    sku: str
    visits_per_day: float
    stock_units: int
    sales_per_day: float
    margin_percent: float
    lead_time_days: int
    financing_requested: bool
    free_shipping: bool
    restricted_return: bool
    extended_warranty: bool

    base_price: float = 100.0
