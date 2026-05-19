import { useCallback, useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { evaluatePricing, fetchProduct } from "../api";
import { useCart } from "../cart/CartContext";
import { ExpertPanel } from "../components/ExpertPanel";
import { MetricsSimulator } from "../components/MetricsSimulator";
import { ProductImage } from "../components/ProductImage";
import { PriceBadge } from "../components/PriceBadge";
import { PropositionStrip } from "../components/PropositionStrip";
import type { MetricsInput, PricingDecisionOut, Product } from "../types";

export default function ProductPage() {
  const { sku } = useParams<{ sku: string }>();
  const { addItem } = useCart();
  const [product, setProduct] = useState<Product | null>(null);
  const [metrics, setMetrics] = useState<MetricsInput | null>(null);
  const [pricing, setPricing] = useState<PricingDecisionOut | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!sku) return;
    fetchProduct(sku)
      .then((p) => {
        setProduct(p);
        setMetrics({ ...p.default_metrics, base_price: p.base_price });
        setPricing(p.pricing);
      })
      .catch((e: Error) => setError(e.message));
  }, [sku]);

  const runEvaluate = useCallback(async (m: MetricsInput) => {
    if (!sku) return;
    const result = await evaluatePricing(sku, m);
    setPricing(result);
  }, [sku]);

  useEffect(() => {
    if (!metrics) return;
    const t = setTimeout(() => {
      runEvaluate(metrics).catch((e: Error) => setError(e.message));
    }, 350);
    return () => clearTimeout(t);
  }, [metrics, runEvaluate]);

  const updateMetric = <K extends keyof MetricsInput>(
    key: K,
    value: MetricsInput[K],
  ) => {
    setMetrics((prev) => (prev ? { ...prev, [key]: value } : prev));
  };

  if (error && !product) {
    return <p className="state-msg error">{error}</p>;
  }
  if (!product || !metrics || !pricing) {
    return <p className="state-msg">Cargando producto…</p>;
  }

  return (
    <section className="product-detail">
      <Link to="/" className="back-link">
        ← Volver a portada
      </Link>
      <header className="section-header">
        <p className="kicker">{product.category}</p>
        <h1 className="headline-main">{product.name}</h1>
        <p className="byline">Ref. {product.sku}</p>
      </header>
      <hr className="rule-thin" />
      <div className="detail-layout">
        <div className="detail-main">
          <ProductImage src={product.image_url} className="detail-image" />
          <p className="article-body">{product.description}</p>
          <PriceBadge pricing={pricing} />
          <PropositionStrip propositions={pricing.propositions} />
          <button
            type="button"
            className="btn btn-primary"
            onClick={() =>
              addItem({
                sku: product.sku,
                name: product.name,
                financing_requested: metrics.financing_requested,
              })
            }
          >
            Anotar en la canasta
          </button>

          <div className="simulator sidebar-box">
            <h2 className="box-head">Crónica de mercado</h2>
            <p className="box-kicker muted">
              Métricas y políticas comerciales → proposiciones DA–GE → reglas 1–11.
            </p>
            <MetricsSimulator metrics={metrics} onChange={updateMetric} />
          </div>
        </div>
        <ExpertPanel pricing={pricing} />
      </div>
    </section>
  );
}
