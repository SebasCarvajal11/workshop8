from abc import ABC, abstractmethod
from typing import Mapping

from .metrics import ProductMetrics

PropositionCode = str
PropositionMap = dict[PropositionCode, bool]

PROPOSITION_CODES: tuple[str, ...] = (
    "DA",
    "DB",
    "OB",
    "VA",
    "VB",
    "MA",
    "MB",
    "TL",
    "PF",
    "EG",
    "DR",
    "GE",
)

INTERVIEW_QUESTIONS: tuple[tuple[str, str], ...] = (
    ("DA", "¿La demanda del producto es alta (ej. más de 1000 visitas/día)?"),
    ("DB", "¿La demanda del producto es baja (ej. menos de 50 visitas/día)?"),
    ("OB", "¿El inventario (oferta) es bajo (ej. menos de 10 unidades)?"),
    ("VA", "¿El volumen de ventas es alto (ej. más de 50 ventas/día)?"),
    ("VB", "¿El volumen de ventas es bajo (ej. menos de 5 ventas/día)?"),
    ("MA", "¿El margen de ganancia es alto (más del 40%)?"),
    ("MB", "¿El margen de ganancia es bajo (menos del 10%)?"),
    ("TL", "¿El lead time de reabasto es largo (más de 15 días)?"),
    ("PF", "¿El cliente solicita financiamiento (pago a plazos)?"),
    ("EG", "¿El producto califica para envío gratis?"),
    ("DR", "¿La política de devolución es restringida (venta final)?"),
    ("GE", "¿El producto incluye garantía extendida?"),
)


class PropositionEvaluator(ABC):
    @abstractmethod
    def evaluate(self, metrics: ProductMetrics) -> PropositionMap:
        raise NotImplementedError


class ThresholdPropositionEvaluator(PropositionEvaluator):
    """Traduce métricas a proposiciones DA…GE según umbrales del enunciado."""

    def evaluate(self, metrics: ProductMetrics) -> PropositionMap:
        return {
            "DA": metrics.visits_per_day > 1000,
            "DB": metrics.visits_per_day < 50,
            "OB": metrics.stock_units < 10,
            "VA": metrics.sales_per_day > 50,
            "VB": metrics.sales_per_day < 5,
            "MA": metrics.margin_percent > 40,
            "MB": metrics.margin_percent < 10,
            "TL": metrics.lead_time_days > 15,
            "PF": metrics.financing_requested,
            "EG": metrics.free_shipping,
            "DR": metrics.restricted_return,
            "GE": metrics.extended_warranty,
        }
