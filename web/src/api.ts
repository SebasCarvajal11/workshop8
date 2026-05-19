import type {
  CartLine,
  CartQuote,
  InterviewQuestion,
  MetricsInput,
  PricingDecisionOut,
  Product,
  PropositionFlags,
} from "./types";

const base = "";

export async function fetchProducts(): Promise<Product[]> {
  const res = await fetch(`${base}/api/products`);
  if (!res.ok) throw new Error("No se pudo cargar el catálogo");
  return res.json();
}

export async function fetchProduct(sku: string): Promise<Product> {
  const res = await fetch(`${base}/api/products/${encodeURIComponent(sku)}`);
  if (!res.ok) throw new Error("Producto no encontrado");
  return res.json();
}

export async function evaluatePricing(
  sku: string,
  metrics: MetricsInput,
  financing_requested?: boolean,
): Promise<PricingDecisionOut> {
  const res = await fetch(`${base}/api/pricing/evaluate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ sku, metrics, financing_requested }),
  });
  if (!res.ok) throw new Error("Error al evaluar precio");
  return res.json();
}

export async function fetchInterviewQuestions(): Promise<InterviewQuestion[]> {
  const res = await fetch(`${base}/api/interview/questions`);
  if (!res.ok) throw new Error("No se pudieron cargar las preguntas");
  return res.json();
}

export async function evaluateInterview(
  sku: string,
  basePrice: number,
  props: PropositionFlags,
): Promise<PricingDecisionOut> {
  const res = await fetch(`${base}/api/pricing/evaluate-interview`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ sku, base_price: basePrice, ...props }),
  });
  if (!res.ok) throw new Error("Error en entrevista CLIPS");
  return res.json();
}

export async function quoteCart(lines: CartLine[]): Promise<CartQuote> {
  const res = await fetch(`${base}/api/cart/quote`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      lines: lines.map((l) => ({
        sku: l.sku,
        quantity: l.quantity,
        financing_requested: l.financing_requested,
      })),
    }),
  });
  if (!res.ok) throw new Error("No se pudo cotizar el carrito");
  return res.json();
}
