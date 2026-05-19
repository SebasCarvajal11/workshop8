from pricing_expert.decision import DiscountAction, PriceChange
from pricing_expert.service import DynamicPricingService


def test_cool_producto_interview_veto_rule_4() -> None:
    service = DynamicPricingService()
    props = {
        "DA": False,
        "DB": True,
        "OB": False,
        "VA": False,
        "VB": True,
        "MA": False,
        "MB": True,
        "TL": False,
        "PF": False,
        "EG": False,
        "DR": True,
        "GE": False,
    }
    decision = service.evaluate_propositions("COOL-1", 200.0, props)
    assert decision.discount == DiscountAction.NO_DISCOUNT


def test_cool_producto_increase_rule_1() -> None:
    service = DynamicPricingService()
    props = {code: False for code in ("DA", "DB", "OB", "VA", "VB", "MA", "MB", "TL", "PF", "EG", "DR", "GE")}
    props["DA"] = True
    props["OB"] = True
    decision = service.evaluate_propositions("COOL-2", 100.0, props)
    assert decision.price_change == PriceChange.INCREASE
