from .decision import PricingDecision
from .engine import ClipsPricingEngine
from .metrics import ProductMetrics
from .propositions import (
    PropositionEvaluator,
    PropositionMap,
    ThresholdPropositionEvaluator,
)


class DynamicPricingService:
    """Fachada de dominio: evalúa proposiciones y consulta el experto CLIPS."""

    def __init__(
        self,
        engine: ClipsPricingEngine | None = None,
        evaluator: PropositionEvaluator | None = None,
    ) -> None:
        self._evaluator = evaluator or ThresholdPropositionEvaluator()
        self._engine = engine or ClipsPricingEngine(
            proposition_evaluator=self._evaluator
        )

    def evaluate_product(self, metrics: ProductMetrics) -> PricingDecision:
        return self._engine.run(metrics, self._evaluator)

    def evaluate_propositions(
        self,
        sku: str,
        base_price: float,
        props: PropositionMap,
    ) -> PricingDecision:
        return self._engine.run_propositions(sku, base_price, props)

    def explain_propositions(self, metrics: ProductMetrics) -> PropositionMap:
        return dict(self._evaluator.evaluate(metrics))
