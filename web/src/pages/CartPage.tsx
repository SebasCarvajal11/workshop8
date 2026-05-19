import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { quoteCart } from "../api";
import { useCart } from "../cart/CartContext";
import { ExpertPanel } from "../components/ExpertPanel";
import type { CartQuote } from "../types";

export default function CartPage() {
  const { items, updateQty, removeItem, setFinancing, clear, count } =
    useCart();
  const [quote, setQuote] = useState<CartQuote | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (items.length === 0) {
      setQuote(null);
      return;
    }
    quoteCart(items)
      .then(setQuote)
      .catch((e: Error) => setError(e.message));
  }, [items]);

  if (count === 0) {
    return (
      <section className="cart-empty">
        <p className="kicker">Canasta del lector</p>
        <h1 className="headline-main">Sin mercancía anotada</h1>
        <p className="deck">
          Visite la portada y seleccione avisos clasificados con precio dinámico.
        </p>
        <Link to="/" className="btn">
          Volver a la portada
        </Link>
      </section>
    );
  }

  return (
    <section className="cart-page">
      <header className="section-header">
        <p className="kicker">Resumen de compra</p>
        <h1 className="headline-main">Su canasta</h1>
      </header>
      <hr className="rule-thin" />
      {error ? <p className="state-msg error">{error}</p> : null}
      <div className="cart-layout">
        <ul className="cart-lines">
          {items.map((line) => {
            const priced = quote?.lines.find((l) => l.sku === line.sku);
            return (
              <li key={line.sku} className="cart-line">
                <div>
                  <Link to={`/product/${encodeURIComponent(line.sku)}`}>
                    {line.name}
                  </Link>
                  <span className="sku">{line.sku}</span>
                </div>
                <div className="line-controls">
                  <label>
                    Cant.
                    <input
                      type="number"
                      min={1}
                      max={99}
                      value={line.quantity}
                      onChange={(e) =>
                        updateQty(line.sku, Number(e.target.value))
                      }
                    />
                  </label>
                  <label>
                    <input
                      type="checkbox"
                      checked={line.financing_requested}
                      onChange={(e) =>
                        setFinancing(line.sku, e.target.checked)
                      }
                    />
                    Financiamiento
                  </label>
                  <button
                    type="button"
                    className="btn-ghost"
                    onClick={() => removeItem(line.sku)}
                  >
                    Quitar
                  </button>
                </div>
                <div className="line-price">
                  {priced ? (
                    <>
                      <strong>${priced.unit_price.toFixed(2)}</strong> c/u
                      <br />
                      <span>Total línea: ${priced.line_total.toFixed(2)}</span>
                    </>
                  ) : (
                    <span className="muted">Calculando…</span>
                  )}
                </div>
                {priced ? <ExpertPanel pricing={priced.pricing} /> : null}
              </li>
            );
          })}
        </ul>
        <aside className="cart-summary">
          <h2>Resumen</h2>
          <p className="total">
            Subtotal:{" "}
            <strong>
              ${quote ? quote.subtotal.toFixed(2) : "—"} {quote?.currency}
            </strong>
          </p>
          <p className="muted">
            Precios recalculados con reglas CLIPS por línea (checkout demo).
          </p>
          <button type="button" className="btn btn-primary" disabled>
            Pagar (demo)
          </button>
          <button type="button" className="btn-ghost" onClick={clear}>
            Vaciar carrito
          </button>
        </aside>
      </div>
    </section>
  );
}
