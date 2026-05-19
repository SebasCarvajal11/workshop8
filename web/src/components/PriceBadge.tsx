import type { PricingDecisionOut } from "../types";

export function PriceBadge({
  pricing,
  compact = false,
}: {
  pricing: PricingDecisionOut;
  compact?: boolean;
}) {
  const hasDiscount = pricing.discount === "APPLY";
  const change = pricing.price_change;

  return (
    <div className={`price-stack${compact ? " price-stack--compact" : ""}`}>
      {!compact &&
      (pricing.final_price < pricing.base_price || hasDiscount) ? (
        <span className="price-old">Ant. ${pricing.base_price.toFixed(2)}</span>
      ) : null}
      <span className="price-current">${pricing.final_price.toFixed(2)}</span>
      <div className="price-tags">
        {change === "INCREASE" ? (
          <span className="tag tag-up">Al alza</span>
        ) : null}
        {change === "DECREASE" ? (
          <span className="tag tag-down">Baja</span>
        ) : null}
        {change === "MIXED" ? <span className="tag tag-mixed">Mixto</span> : null}
        {hasDiscount ? (
          <span className="tag tag-discount">-{pricing.discount_pct}%</span>
        ) : null}
      </div>
    </div>
  );
}
