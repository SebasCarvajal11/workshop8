import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import {
  evaluateInterview,
  fetchInterviewQuestions,
  fetchProducts,
} from "../api";
import { ExpertPanel } from "../components/ExpertPanel";
import { PriceBadge } from "../components/PriceBadge";
import { PropositionStrip } from "../components/PropositionStrip";
import type { InterviewQuestion, PricingDecisionOut, Product } from "../types";

const PROP_KEYS = [
  "DA",
  "DB",
  "OB",
  "VA",
  "VB",
  "MA",
  "MB",
  "TL",
  "PF",
  "EG",
  "DR",
  "GE",
] as const;

type PropKey = (typeof PROP_KEYS)[number];

const initialProps = (): Record<PropKey, boolean> =>
  Object.fromEntries(PROP_KEYS.map((k) => [k, false])) as Record<
    PropKey,
    boolean
  >;

export default function InterviewPage() {
  const [questions, setQuestions] = useState<InterviewQuestion[]>([]);
  const [catalog, setCatalog] = useState<Product[]>([]);
  const [props, setProps] = useState(initialProps);
  const [sku, setSku] = useState("SKU-LAP-01");
  const [basePrice, setBasePrice] = useState(1299);
  const [pricing, setPricing] = useState<PricingDecisionOut | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([fetchInterviewQuestions(), fetchProducts()])
      .then(([q, products]) => {
        setQuestions(q);
        setCatalog(products);
        if (products[0]) {
          setSku(products[0].sku);
          setBasePrice(products[0].base_price);
        }
      })
      .catch((e: Error) => setError(e.message));
  }, []);

  const submit = async () => {
    setError(null);
    try {
      const result = await evaluateInterview(sku, basePrice, props);
      setPricing(result);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Error");
    }
  };

  return (
    <section className="interview-page">
      <Link to="/" className="back-link">
        ← Volver a portada
      </Link>
      <header className="section-header">
        <p className="kicker">Suplemento académico · Workshop 5</p>
        <h1 className="headline-main">Entrevista al sistema experto</h1>
        <p className="deck">
          Las 12 proposiciones (DA–GE) alimentan <code>Producto</code> (COOL) y
          las 11 reglas del taller.
        </p>
      </header>
      <hr className="rule-thin" />
      <div className="interview-layout">
        <div className="interview-form">
          {catalog.length > 0 ? (
            <label>
              Producto del catálogo
              <select
                className="text-input"
                value={sku}
                onChange={(e) => {
                  const next = catalog.find((p) => p.sku === e.target.value);
                  setSku(e.target.value);
                  if (next) setBasePrice(next.base_price);
                }}
              >
                {catalog.map((p) => (
                  <option key={p.sku} value={p.sku}>
                    {p.name} ({p.sku})
                  </option>
                ))}
              </select>
            </label>
          ) : null}
          <label>
            SKU
            <input
              value={sku}
              readOnly
              className="text-input text-input--readonly"
            />
          </label>
          <label>
            Precio base (USD)
            <input
              type="number"
              min={1}
              value={basePrice}
              onChange={(e) => setBasePrice(Number(e.target.value))}
              className="text-input"
            />
          </label>
          <ul className="interview-list">
            {questions.map((q) => (
              <li key={q.code}>
                <label>
                  <input
                    type="checkbox"
                    checked={props[q.code as PropKey]}
                    onChange={(e) =>
                      setProps((prev) => ({
                        ...prev,
                        [q.code]: e.target.checked,
                      }))
                    }
                  />
                  <span>
                    <strong>{q.code}</strong> — {q.question}
                  </span>
                </label>
              </li>
            ))}
          </ul>
          <button type="button" className="btn btn-primary" onClick={submit}>
            Ejecutar motor CLIPS
          </button>
          {error ? <p className="state-msg error">{error}</p> : null}
        </div>
        {pricing ? (
          <div className="interview-result">
            <PriceBadge pricing={pricing} />
            <PropositionStrip propositions={pricing.propositions} />
            <ExpertPanel pricing={pricing} />
          </div>
        ) : null}
      </div>
    </section>
  );
}
