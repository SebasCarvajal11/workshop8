import pytest

from pricing_expert.decision import DiscountAction, PriceChange
from pricing_expert.metrics import ProductMetrics
from pricing_expert.service import DynamicPricingService


@pytest.fixture
def service() -> DynamicPricingService:
    return DynamicPricingService()


def test_rule_1_increase_high_demand_low_stock(service: DynamicPricingService) -> None:
    m = ProductMetrics(
        sku="R1",
        visits_per_day=1500,
        stock_units=5,
        sales_per_day=30,
        margin_percent=25,
        lead_time_days=5,
        financing_requested=False,
        free_shipping=False,
        restricted_return=False,
        extended_warranty=False,
    )
    d = service.evaluate_product(m)
    assert d.price_change == PriceChange.INCREASE
    assert d.price_delta_pct == 10.0


def test_rule_4_veto_discount_overrides_apply(service: DynamicPricingService) -> None:
    """Margen bajo (MB) anula descuentos sugeridos por otras reglas."""
    m = ProductMetrics(
        sku="R4",
        visits_per_day=30,
        stock_units=100,
        sales_per_day=2,
        margin_percent=5,
        lead_time_days=5,
        financing_requested=False,
        free_shipping=False,
        restricted_return=True,
        extended_warranty=False,
    )
    d = service.evaluate_product(m)
    assert d.discount == DiscountAction.NO_DISCOUNT


def test_rule_10_veto_discount_low_stock_high_demand(service: DynamicPricingService) -> None:
    m = ProductMetrics(
        sku="R10",
        visits_per_day=2000,
        stock_units=3,
        sales_per_day=2,
        margin_percent=30,
        lead_time_days=5,
        financing_requested=False,
        free_shipping=False,
        restricted_return=False,
        extended_warranty=True,
    )
    d = service.evaluate_product(m)
    assert d.discount == DiscountAction.NO_DISCOUNT


def test_rule_8_decrease_price(service: DynamicPricingService) -> None:
    m = ProductMetrics(
        sku="R8",
        visits_per_day=200,
        stock_units=50,
        sales_per_day=2,
        margin_percent=30,
        lead_time_days=5,
        financing_requested=False,
        free_shipping=False,
        restricted_return=False,
        extended_warranty=False,
    )
    d = service.evaluate_product(m)
    assert PriceChange.DECREASE in (d.price_change,)
    assert d.price_delta_pct <= -10.0
