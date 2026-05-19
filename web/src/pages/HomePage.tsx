import { useCallback, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { evaluatePricing, fetchProducts } from "../api";
import { useCart } from "../cart/CartContext";
import { ExpertPanel } from "../components/ExpertPanel";
import { MetricsSimulator } from "../components/MetricsSimulator";
import { ProductImage } from "../components/ProductImage";
import { PriceBadge } from "../components/PriceBadge";
import { PropositionStrip } from "../components/PropositionStrip";
import type { MetricsInput, Product } from "../types";

function metricsForProduct(p: Product): MetricsInput {
  return {
    ...p.default_metrics,
    base_price: p.base_price,
  };
}

export default function HomePage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeSku, setActiveSku] = useState<string | null>(null);
  const [metrics, setMetrics] = useState<MetricsInput | null>(null);
  const { addItem, items, count } = useCart();

  useEffect(() => {
    fetchProducts()
      .then((list) => {
        setProducts(list);
        if (list[0]) {
          setActiveSku(list[0].sku);
          setMetrics(metricsForProduct(list[0]));
        }
      })
      .catch((e: Error) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  const active = products.find((p) => p.sku === activeSku) ?? products[0];

  const refreshPricing = useCallback(
    async (sku: string, m: MetricsInput) => {
      const pricing = await evaluatePricing(sku, m);
      setProducts((prev) =>
        prev.map((p) => (p.sku === sku ? { ...p, pricing } : p)),
      );
    },
    [],
  );

  useEffect(() => {
    if (!active || !metrics) return;
    const m = { ...metrics, base_price: active.base_price };
    const t = setTimeout(() => {
      refreshPricing(active.sku, m).catch(() => undefined);
    }, 300);
    return () => clearTimeout(t);
  }, [active, metrics, refreshPricing]);

  const selectProduct = (p: Product) => {
    setActiveSku(p.sku);
    setMetrics(metricsForProduct(p));
  };

  const updateMetric = <K extends keyof MetricsInput>(
    key: K,
    value: MetricsInput[K],
  ) => {
    setMetrics((prev) => (prev ? { ...prev, [key]: value } : prev));
  };

  if (loading) {
    return (
      <div className="viewport-state" role="status">
        <p className="kicker">Edición en curso</p>
        <p className="state-msg">Cargando cotizaciones…</p>
      </div>
    );
  }
  if (error) {
    return (
      <div className="viewport-state viewport-state--error" role="alert">
        <p className="kicker">Aviso al lector</p>
        <p className="state-msg error">
          {error}. Inicie la API en el puerto 8000.
        </p>
      </div>
    );
  }

  return (
    <section className="viewport-page" aria-label="Bolsa de precios">
      <div className="viewport-grid">
        <div className="product-wall-wrap">
          <header className="wall-header">
            <span className="wall-header__label">Listado</span>
            <h2 className="wall-header__title">Ítems en cotización</h2>
          </header>
          <div className="product-wall" role="list">
            {products.map((p) => (
              <article
                key={p.sku}
                className={`product-tile${p.sku === active?.sku ? " is-active" : ""}`}
                onClick={() => selectProduct(p)}
                onKeyDown={(e) => e.key === "Enter" && selectProduct(p)}
                role="listitem"
                tabIndex={0}
                aria-selected={p.sku === active?.sku}
                aria-label={`Seleccionar ${p.name}`}
              >
                <div className="tile-image">
                  <ProductImage src={p.image_url} />
                </div>
                <div className="tile-caption">
                  <h3 className="tile-title">{p.name}</h3>
                  <PriceBadge pricing={p.pricing} compact />
                  <Link
                    to={`/product/${encodeURIComponent(p.sku)}`}
                    className="tile-detail-link"
                    onClick={(e) => e.stopPropagation()}
                  >
                    Ver ficha completa
                  </Link>
                </div>
              </article>
            ))}
          </div>
        </div>

        <aside className="viewport-side" aria-label="Detalle y simulador">
          {active && metrics ? (
            <div className="viewport-side-inner">
              <header className="panel-section panel-section--lead">
                <p className="kicker">{active.category}</p>
                <h2 className="side-headline">{active.name}</h2>
                <p className="byline">Ref. {active.sku}</p>
                <PriceBadge pricing={active.pricing} />
                <PropositionStrip
                  propositions={active.pricing.propositions}
                  compact
                />
              </header>

              <section className="panel-section" aria-labelledby="sim-heading">
                <h3 id="sim-heading" className="panel-section-title">
                  Simulador de métricas
                </h3>
                <p className="panel-section-hint">
                  Umbrales del taller (visitas, stock, ventas, margen, lead time)
                  y flags PF, EG, DR, GE alimentan las 11 reglas CLIPS.
                </p>
                <MetricsSimulator
                  metrics={metrics}
                  onChange={updateMetric}
                  variant="compact"
                />
              </section>

              <div className="panel-section panel-section--actions">
                <Link
                  to={`/product/${encodeURIComponent(active.sku)}`}
                  className="btn btn-block"
                >
                  Abrir ficha del producto
                </Link>
                <button
                  type="button"
                  className="btn btn-primary btn-block"
                  onClick={() =>
                    addItem({
                      sku: active.sku,
                      name: active.name,
                      financing_requested: metrics.financing_requested,
                    })
                  }
                >
                  Añadir a la canasta · {count}{" "}
                  {count === 1 ? "artículo" : "artículos"}
                </button>
              </div>

              <section className="panel-section panel-section--expert">
                <ExpertPanel pricing={active.pricing} compact />
              </section>
            </div>
          ) : null}
        </aside>
      </div>

      {items.length > 0 ? (
        <footer className="viewport-cart" aria-label="Resumen de canasta">
          <span className="viewport-cart__label">Canasta</span>
          <span className="viewport-cart__lines">
            {items.map((i) => `${i.name} ×${i.quantity}`).join(" · ")}
          </span>
          <Link to="/canasta" className="viewport-cart__link">
            Ver canasta →
          </Link>
        </footer>
      ) : null}
    </section>
  );
}
