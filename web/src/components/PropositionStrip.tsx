import type { PropositionOut } from "../types";

const ORDER = [
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

export function PropositionStrip({
  propositions,
  compact = false,
}: {
  propositions: PropositionOut[];
  compact?: boolean;
}) {
  const byCode = Object.fromEntries(
    propositions.map((p) => [p.code, p.active]),
  );

  return (
    <div
      className={`prop-strip${compact ? " prop-strip--compact" : ""}`}
      aria-label="Proposiciones activas (DA–GE)"
    >
      <p className="prop-strip__title">Proposiciones CLIPS</p>
      <ul className="prop-strip__list">
        {ORDER.map((code) => {
          const active = byCode[code] ?? false;
          return (
            <li
              key={code}
              className={`prop-chip${active ? " prop-chip--on" : ""}`}
              title={active ? "Activa" : "Inactiva"}
            >
              {code}
            </li>
          );
        })}
      </ul>
    </div>
  );
}
