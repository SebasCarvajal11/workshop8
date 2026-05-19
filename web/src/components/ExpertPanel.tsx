import type { PricingDecisionOut } from "../types";

export function ExpertPanel({
  pricing,
  compact = false,
}: {
  pricing: PricingDecisionOut;
  compact?: boolean;
}) {
  const active = pricing.propositions.filter((p) => p.active);

  return (
    <aside
      className={`expert-panel sidebar-box${compact ? " expert-panel--compact" : ""}`}
    >
      <h3 className="box-head">Despacho del experto</h3>
      <p className="box-kicker">CLIPS · reglas de negocio</p>
      <p className="muted">
        Reglas disparadas:{" "}
        <strong>{pricing.fired_rules || "ninguna"}</strong>
      </p>
      <ul className="prop-list">
        {active.length === 0 ? (
          <li className="muted">Sin proposiciones activas</li>
        ) : (
          active.map((p) => (
            <li key={p.code}>
              <code>{p.code}</code>
            </li>
          ))
        )}
      </ul>
      <dl className="decision-dl">
        <dt>Cambio precio</dt>
        <dd>
          {pricing.price_change} ({pricing.price_delta_pct >= 0 ? "+" : ""}
          {pricing.price_delta_pct}%)
        </dd>
        <dt>Descuento</dt>
        <dd>
          {pricing.discount === "APPLY"
            ? `Sí (${pricing.discount_pct}%)`
            : "No"}
        </dd>
      </dl>
    </aside>
  );
}
