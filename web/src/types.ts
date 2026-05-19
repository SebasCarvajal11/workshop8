export interface MetricsInput {
  visits_per_day: number;
  stock_units: number;
  sales_per_day: number;
  margin_percent: number;
  lead_time_days: number;
  financing_requested: boolean;
  free_shipping: boolean;
  restricted_return: boolean;
  extended_warranty: boolean;
  base_price: number;
}

export interface PropositionOut {
  code: string;
  active: boolean;
}

export interface PricingDecisionOut {
  sku: string;
  base_price: number;
  final_price: number;
  price_change: string;
  price_delta_pct: number;
  discount: string;
  discount_pct: number;
  fired_rules: string;
  propositions: PropositionOut[];
}

export interface Product {
  sku: string;
  name: string;
  description: string;
  category: string;
  image_url: string;
  base_price: number;
  default_metrics: MetricsInput;
  pricing: PricingDecisionOut;
}

export interface CartLine {
  sku: string;
  name: string;
  quantity: number;
  financing_requested: boolean;
}

export interface CartLineOut {
  sku: string;
  name: string;
  quantity: number;
  unit_price: number;
  line_total: number;
  pricing: PricingDecisionOut;
}

export interface CartQuote {
  lines: CartLineOut[];
  subtotal: number;
  currency: string;
}

export interface InterviewQuestion {
  code: string;
  question: string;
}

export type PropositionFlags = Record<
  "DA" | "DB" | "OB" | "VA" | "VB" | "MA" | "MB" | "TL" | "PF" | "EG" | "DR" | "GE",
  boolean
>;
