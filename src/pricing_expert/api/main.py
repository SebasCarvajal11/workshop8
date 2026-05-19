from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from pricing_expert.api.schemas import (
    CartLineOut,
    CartQuoteOut,
    CartQuoteRequest,
    InterviewEvaluateRequest,
    InterviewQuestionOut,
    MetricsInput,
    PricingDecisionOut,
    PricingEvaluateRequest,
    ProductOut,
    PropositionOut,
)
from pricing_expert.propositions import INTERVIEW_QUESTIONS
from pricing_expert.catalog import get_product, list_products
from pricing_expert.catalog_media import sync_product_images
from pricing_expert.decision import PricingDecision
from pricing_expert.metrics import ProductMetrics
from pricing_expert.service import DynamicPricingService

app = FastAPI(
    title="Tienda experta — precios dinámicos",
    description="E-commerce con motor de reglas CLIPS",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_service = DynamicPricingService()


@app.on_event("startup")
def _startup_sync_product_images() -> None:
    sync_product_images()


def _metrics_from_input(sku: str, base_price: float, m: MetricsInput) -> ProductMetrics:
    return ProductMetrics(
        sku=sku,
        visits_per_day=m.visits_per_day,
        stock_units=m.stock_units,
        sales_per_day=m.sales_per_day,
        margin_percent=m.margin_percent,
        lead_time_days=m.lead_time_days,
        financing_requested=m.financing_requested,
        free_shipping=m.free_shipping,
        restricted_return=m.restricted_return,
        extended_warranty=m.extended_warranty,
        base_price=base_price,
    )


def _metrics_to_input(m: ProductMetrics) -> MetricsInput:
    return MetricsInput(
        visits_per_day=m.visits_per_day,
        stock_units=m.stock_units,
        sales_per_day=m.sales_per_day,
        margin_percent=m.margin_percent,
        lead_time_days=m.lead_time_days,
        financing_requested=m.financing_requested,
        free_shipping=m.free_shipping,
        restricted_return=m.restricted_return,
        extended_warranty=m.extended_warranty,
        base_price=m.base_price,
    )


def _decision_out(
    decision: PricingDecision, props: dict[str, bool], base_price: float
) -> PricingDecisionOut:
    return PricingDecisionOut(
        sku=decision.sku,
        base_price=base_price,
        final_price=decision.final_price,
        price_change=decision.price_change.value,
        price_delta_pct=decision.price_delta_pct,
        discount=decision.discount.value,
        discount_pct=decision.discount_pct,
        fired_rules=decision.fired_rules,
        propositions=[
            PropositionOut(code=k, active=v) for k, v in sorted(props.items())
        ],
    )


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "engine": "clips", "model": "defclass Producto"}


@app.get("/api/interview/questions", response_model=list[InterviewQuestionOut])
def api_interview_questions() -> list[InterviewQuestionOut]:
    return [
        InterviewQuestionOut(code=code, question=q)
        for code, q in INTERVIEW_QUESTIONS
    ]


@app.post("/api/pricing/evaluate-interview", response_model=PricingDecisionOut)
def api_evaluate_interview(body: InterviewEvaluateRequest) -> PricingDecisionOut:
    p = get_product(body.sku)
    base = body.base_price if p is None else p.base_price
    sku = body.sku
    props = body.to_proposition_map()
    decision = _service.evaluate_propositions(sku, base, props)
    return _decision_out(decision, props, base)


@app.get("/api/products", response_model=list[ProductOut])
def api_list_products() -> list[ProductOut]:
    out: list[ProductOut] = []
    for p in list_products():
        props = _service.explain_propositions(p.default_metrics)
        decision = _service.evaluate_product(p.default_metrics)
        out.append(
            ProductOut(
                sku=p.sku,
                name=p.name,
                description=p.description,
                category=p.category,
                image_url=p.image_url,
                base_price=p.base_price,
                default_metrics=_metrics_to_input(p.default_metrics),
                pricing=_decision_out(decision, props, p.base_price),
            )
        )
    return out


@app.get("/api/products/{sku}", response_model=ProductOut)
def api_get_product(sku: str) -> ProductOut:
    p = get_product(sku)
    if not p:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    props = _service.explain_propositions(p.default_metrics)
    decision = _service.evaluate_product(p.default_metrics)
    return ProductOut(
        sku=p.sku,
        name=p.name,
        description=p.description,
        category=p.category,
        image_url=p.image_url,
        base_price=p.base_price,
        default_metrics=_metrics_to_input(p.default_metrics),
        pricing=_decision_out(decision, props, p.base_price),
    )


@app.post("/api/pricing/evaluate", response_model=PricingDecisionOut)
def api_evaluate(body: PricingEvaluateRequest) -> PricingDecisionOut:
    p = get_product(body.sku)
    if not p:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    if body.metrics:
        m_in = body.metrics
        if body.financing_requested is not None:
            m_in = m_in.model_copy(
                update={"financing_requested": body.financing_requested}
            )
        metrics = _metrics_from_input(p.sku, p.base_price, m_in)
    else:
        metrics = p.default_metrics
        if body.financing_requested is not None:
            metrics = ProductMetrics(
                **{
                    **metrics.__dict__,
                    "financing_requested": body.financing_requested,
                }
            )

    props = _service.explain_propositions(metrics)
    decision = _service.evaluate_product(metrics)
    return _decision_out(decision, props, p.base_price)


@app.post("/api/cart/quote", response_model=CartQuoteOut)
def api_cart_quote(body: CartQuoteRequest) -> CartQuoteOut:
    lines_out: list[CartLineOut] = []
    subtotal = 0.0

    for line in body.lines:
        p = get_product(line.sku)
        if not p:
            raise HTTPException(status_code=404, detail=f"SKU desconocido: {line.sku}")

        metrics = ProductMetrics(
            **{
                **p.default_metrics.__dict__,
                "financing_requested": line.financing_requested,
            }
        )
        props = _service.explain_propositions(metrics)
        decision = _service.evaluate_product(metrics)
        line_total = round(decision.final_price * line.quantity, 2)
        subtotal += line_total
        lines_out.append(
            CartLineOut(
                sku=p.sku,
                name=p.name,
                quantity=line.quantity,
                unit_price=decision.final_price,
                line_total=line_total,
                pricing=_decision_out(decision, props, p.base_price),
            )
        )

    return CartQuoteOut(lines=lines_out, subtotal=round(subtotal, 2))


_project_root = Path(__file__).resolve().parents[3]
_products_public = _project_root / "web" / "public" / "products"
if _products_public.is_dir():
    app.mount(
        "/products",
        StaticFiles(directory=str(_products_public)),
        name="catalog-products",
    )

_web_dist = _project_root / "web" / "dist"
if _web_dist.is_dir():
    app.mount("/", StaticFiles(directory=str(_web_dist), html=True), name="web")
