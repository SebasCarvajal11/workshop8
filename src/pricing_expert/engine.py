from pathlib import Path

import clips

from .decision import DiscountAction, PriceChange, PricingDecision
from .metrics import ProductMetrics
from .propositions import PROPOSITION_CODES, PropositionEvaluator, PropositionMap


class ClipsPricingEngine:
    """Motor de inferencia: carga reglas CLIPS y ejecuta el ciclo de producción."""

    def __init__(
        self,
        rules_path: Path | None = None,
        proposition_evaluator: PropositionEvaluator | None = None,
    ) -> None:
        root = Path(__file__).resolve().parents[2]
        self._rules_path = rules_path or (root / "clips" / "pricing-rules.clp")
        self._proposition_evaluator = proposition_evaluator
        self._env: clips.Environment | None = None

    def _ensure_environment(self) -> clips.Environment:
        if self._env is None:
            env = clips.Environment()
            env.load(str(self._rules_path))
            self._env = env
        return self._env

    def run(
        self,
        metrics: ProductMetrics,
        evaluator: PropositionEvaluator | None = None,
    ) -> PricingDecision:
        ev = evaluator or self._proposition_evaluator
        if ev is None:
            raise ValueError("Se requiere un PropositionEvaluator")
        props: PropositionMap = dict(ev.evaluate(metrics))
        return self.run_propositions(metrics.sku, metrics.base_price, props)

    def run_propositions(
        self,
        sku: str,
        base_price: float,
        props: PropositionMap,
    ) -> PricingDecision:
        env = self._ensure_environment()
        env.reset()
        self._assert_producto(env, sku, props)
        env.run()
        metrics = ProductMetrics(
            sku=sku,
            visits_per_day=0,
            stock_units=0,
            sales_per_day=0,
            margin_percent=0,
            lead_time_days=0,
            financing_requested=props.get("PF", False),
            free_shipping=props.get("EG", False),
            restricted_return=props.get("DR", False),
            extended_warranty=props.get("GE", False),
            base_price=base_price,
        )
        return self._consolidate(env, metrics)

    @staticmethod
    def _sym(value: bool) -> str:
        return "TRUE" if value else "FALSE"

    def _assert_producto(
        self, env: clips.Environment, sku: str, props: PropositionMap
    ) -> None:
        producto_cls = env.find_class("Producto")
        slot_values: dict[str, clips.Symbol | str] = {
            "codigo": sku.replace('"', ""),
        }
        for code in PROPOSITION_CODES:
            slot_values[code.lower()] = clips.Symbol(
                self._sym(bool(props.get(code, False)))
            )
        producto_cls.make_instance("prod", **slot_values)

    def _consolidate(
        self, env: clips.Environment, metrics: ProductMetrics
    ) -> PricingDecision:
        increases = 0
        decreases = 0
        apply_count = 0
        veto = False
        fired: list[str] = []

        for fact in env.facts():
            name = fact.template.name
            if name == "price-signal":
                rule_id = int(fact["rule-id"])
                fired.append(f"P{rule_id}")
                if str(fact["kind"]) == "INCREASE":
                    increases += 1
                else:
                    decreases += 1
            elif name == "discount-signal":
                rule_id = int(fact["rule-id"])
                fired.append(f"D{rule_id}")
                kind = str(fact["kind"])
                if kind == "NO_DISCOUNT" and rule_id in (4, 10):
                    veto = True
                elif kind == "APPLY":
                    apply_count += 1

        if increases > 0 and decreases > 0:
            price_change = PriceChange.MIXED
            delta = 0.0
        elif increases > 0:
            price_change = PriceChange.INCREASE
            delta = 10.0 * increases
        elif decreases > 0:
            price_change = PriceChange.DECREASE
            delta = -10.0 * decreases
        else:
            price_change = PriceChange.NONE
            delta = 0.0

        if veto:
            discount = DiscountAction.NO_DISCOUNT
            disc_pct = 0.0
        elif apply_count > 0:
            discount = DiscountAction.APPLY
            disc_pct = 5.0
        else:
            discount = DiscountAction.NO_DISCOUNT
            disc_pct = 0.0

        final = self._compute_final_price(
            metrics.base_price, price_change, delta, discount, disc_pct
        )
        return PricingDecision(
            price_change=price_change,
            price_delta_pct=delta,
            discount=discount,
            discount_pct=disc_pct,
            fired_rules=" ".join(sorted(set(fired))),
            final_price=final,
            sku=metrics.sku,
        )

    @staticmethod
    def _compute_final_price(
        base: float,
        price_change: PriceChange,
        delta_pct: float,
        discount: DiscountAction,
        discount_pct: float,
    ) -> float:
        price = base
        if price_change == PriceChange.INCREASE:
            price *= 1.0 + abs(delta_pct) / 100.0
        elif price_change == PriceChange.DECREASE:
            price *= 1.0 - abs(delta_pct) / 100.0
        if discount == DiscountAction.APPLY:
            price *= 1.0 - discount_pct / 100.0
        return round(price, 2)
