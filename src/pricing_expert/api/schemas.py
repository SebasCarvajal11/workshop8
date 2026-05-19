from pydantic import BaseModel, Field


class MetricsInput(BaseModel):
    visits_per_day: float = Field(ge=0)
    stock_units: int = Field(ge=0)
    sales_per_day: float = Field(ge=0)
    margin_percent: float = Field(ge=0, le=100)
    lead_time_days: int = Field(ge=0)
    financing_requested: bool = False
    free_shipping: bool = False
    restricted_return: bool = False
    extended_warranty: bool = False
    base_price: float = Field(gt=0)


class PricingEvaluateRequest(BaseModel):
    sku: str
    metrics: MetricsInput | None = None
    financing_requested: bool | None = None


class PropositionOut(BaseModel):
    code: str
    active: bool


class PricingDecisionOut(BaseModel):
    sku: str
    base_price: float
    final_price: float
    price_change: str
    price_delta_pct: float
    discount: str
    discount_pct: float
    fired_rules: str
    propositions: list[PropositionOut]


class ProductOut(BaseModel):
    sku: str
    name: str
    description: str
    category: str
    image_url: str
    base_price: float
    default_metrics: MetricsInput
    pricing: PricingDecisionOut


class CartLineIn(BaseModel):
    sku: str
    quantity: int = Field(ge=1, le=99)
    financing_requested: bool = False


class CartQuoteRequest(BaseModel):
    lines: list[CartLineIn]


class CartLineOut(BaseModel):
    sku: str
    name: str
    quantity: int
    unit_price: float
    line_total: float
    pricing: PricingDecisionOut


class CartQuoteOut(BaseModel):
    lines: list[CartLineOut]
    subtotal: float
    currency: str = "USD"


class InterviewQuestionOut(BaseModel):
    code: str
    question: str


class InterviewEvaluateRequest(BaseModel):
    sku: str = "DEMO-001"
    base_price: float = Field(gt=0, default=100.0)
    DA: bool = False
    DB: bool = False
    OB: bool = False
    VA: bool = False
    VB: bool = False
    MA: bool = False
    MB: bool = False
    TL: bool = False
    PF: bool = False
    EG: bool = False
    DR: bool = False
    GE: bool = False

    def to_proposition_map(self) -> dict[str, bool]:
        return {
            "DA": self.DA,
            "DB": self.DB,
            "OB": self.OB,
            "VA": self.VA,
            "VB": self.VB,
            "MA": self.MA,
            "MB": self.MB,
            "TL": self.TL,
            "PF": self.PF,
            "EG": self.EG,
            "DR": self.DR,
            "GE": self.GE,
        }
