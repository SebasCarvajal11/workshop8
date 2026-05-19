import type { MetricsInput } from "../types";

type Props = {
  metrics: MetricsInput;
  onChange: <K extends keyof MetricsInput>(
    key: K,
    value: MetricsInput[K],
  ) => void;
  variant?: "compact" | "full";
};

export function MetricsSimulator({
  metrics,
  onChange,
  variant = "full",
}: Props) {
  const simClass =
    variant === "compact" ? "mini-sim mini-sim--compact" : "mini-sim";

  return (
    <div className={simClass}>
      <label className="range-field">
        <span className="range-field__label">
          Visitas / día (DA &gt;1000 · DB &lt;50)
          <span className="range-field__value">
            {Math.round(metrics.visits_per_day)}
          </span>
        </span>
        <input
          type="range"
          min={0}
          max={2500}
          step={variant === "compact" ? 50 : 10}
          value={metrics.visits_per_day}
          onChange={(e) =>
            onChange("visits_per_day", Number(e.target.value))
          }
        />
      </label>
      <label className="range-field">
        <span className="range-field__label">
          Stock (OB &lt;10)
          <span className="range-field__value">{metrics.stock_units}</span>
        </span>
        <input
          type="range"
          min={0}
          max={120}
          value={metrics.stock_units}
          onChange={(e) => onChange("stock_units", Number(e.target.value))}
        />
      </label>
      <label className="range-field">
        <span className="range-field__label">
          Ventas / día (VA &gt;50 · VB &lt;5)
          <span className="range-field__value">{metrics.sales_per_day}</span>
        </span>
        <input
          type="range"
          min={0}
          max={80}
          step={1}
          value={metrics.sales_per_day}
          onChange={(e) => onChange("sales_per_day", Number(e.target.value))}
        />
      </label>
      <label className="range-field">
        <span className="range-field__label">
          Margen % (MA &gt;40 · MB &lt;10)
          <span className="range-field__value">{metrics.margin_percent}</span>
        </span>
        <input
          type="range"
          min={0}
          max={60}
          value={metrics.margin_percent}
          onChange={(e) => onChange("margin_percent", Number(e.target.value))}
        />
      </label>
      <label className="range-field">
        <span className="range-field__label">
          Lead time días (TL &gt;15)
          <span className="range-field__value">{metrics.lead_time_days}</span>
        </span>
        <input
          type="range"
          min={1}
          max={30}
          value={metrics.lead_time_days}
          onChange={(e) => onChange("lead_time_days", Number(e.target.value))}
        />
      </label>
      <div className="metric-flags">
        <label className="metric-flag">
          <input
            type="checkbox"
            checked={metrics.financing_requested}
            onChange={(e) =>
              onChange("financing_requested", e.target.checked)
            }
          />
          <span>PF — Financiamiento</span>
        </label>
        <label className="metric-flag">
          <input
            type="checkbox"
            checked={metrics.free_shipping}
            onChange={(e) => onChange("free_shipping", e.target.checked)}
          />
          <span>EG — Envío gratis</span>
        </label>
        <label className="metric-flag">
          <input
            type="checkbox"
            checked={metrics.restricted_return}
            onChange={(e) =>
              onChange("restricted_return", e.target.checked)
            }
          />
          <span>DR — Devolución restringida</span>
        </label>
        <label className="metric-flag">
          <input
            type="checkbox"
            checked={metrics.extended_warranty}
            onChange={(e) =>
              onChange("extended_warranty", e.target.checked)
            }
          />
          <span>GE — Garantía extendida</span>
        </label>
      </div>
    </div>
  );
}
