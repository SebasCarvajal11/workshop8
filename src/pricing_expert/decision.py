from dataclasses import dataclass
from enum import Enum


class PriceChange(str, Enum):
    NONE = "NONE"
    INCREASE = "INCREASE"
    DECREASE = "DECREASE"
    MIXED = "MIXED"


class DiscountAction(str, Enum):
    APPLY = "APPLY"
    NO_DISCOUNT = "NO_DISCOUNT"


@dataclass(frozen=True)
class PricingDecision:
    price_change: PriceChange
    price_delta_pct: float
    discount: DiscountAction
    discount_pct: float
    fired_rules: str
    final_price: float
    sku: str

    def summary_lines(self) -> list[str]:
        lines = [
            f"SKU: {self.sku}",
            f"Cambio de precio: {self.price_change.value} ({self.price_delta_pct:+.1f}%)",
            f"Precio final sugerido: {self.final_price:.2f}",
            f"Descuento: {self.discount.value}",
        ]
        if self.discount == DiscountAction.APPLY:
            lines.append(f"  Cupón: {self.discount_pct:.1f}%")
        if self.fired_rules.strip():
            lines.append(f"Reglas disparadas: {self.fired_rules.strip()}")
        return lines
