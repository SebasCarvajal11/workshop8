"""Interfaz de consola para el sistema experto de precios."""

from __future__ import annotations

import argparse
import sys

from .interview import run_proposition_interview
from .metrics import ProductMetrics
from .service import DynamicPricingService


def _prompt_float(label: str, default: float) -> float:
    raw = input(f"{label} [{default}]: ").strip()
    if not raw:
        return default
    return float(raw)


def _prompt_int(label: str, default: int) -> int:
    raw = input(f"{label} [{default}]: ").strip()
    if not raw:
        return default
    return int(raw)


def _prompt_bool(label: str, default: bool) -> bool:
    d = "s" if default else "n"
    raw = input(f"{label} (s/n) [{d}]: ").strip().lower()
    if not raw:
        return default
    return raw in ("s", "si", "y", "yes", "1")


def _print_result(
    service: DynamicPricingService,
    sku: str,
    props: dict[str, bool],
    decision,
) -> None:
    print("\n--- Proposiciones activas (TRUE) ---")
    for code, active in sorted(props.items()):
        if active:
            print(f"  {code}")

    print("\n--- Recomendación del motor CLIPS (clase Producto) ---")
    for line in decision.summary_lines():
        print(line)


def run_interview_mode() -> int:
    print("=== Sistema experto de precios dinámicos (CLIPS + COOL) ===")
    sku = input("\nSKU del producto [DEMO-001]: ").strip() or "DEMO-001"
    base = _prompt_float("Precio base (USD)", 100.0)
    props = run_proposition_interview()
    service = DynamicPricingService()
    decision = service.evaluate_propositions(sku, base, props)
    _print_result(service, sku, props, decision)
    return 0


def run_metrics_mode() -> int:
    print("=== Modo métricas operativas (derivación automática a proposiciones) ===\n")
    sku = input("SKU del producto [DEMO-001]: ").strip() or "DEMO-001"
    base = _prompt_float("Precio base", 100.0)
    visits = _prompt_float("Visitas por día", 1200.0)
    stock = _prompt_int("Unidades en inventario", 8)
    sales = _prompt_float("Ventas por día", 3.0)
    margin = _prompt_float("Margen de ganancia (%)", 45.0)
    lead = _prompt_int("Lead time de reabasto (días)", 20)
    financing = _prompt_bool("¿Cliente solicita financiamiento?", False)
    shipping = _prompt_bool("¿Califica envío gratis?", True)
    restricted = _prompt_bool("¿Política de devolución restringida?", False)
    warranty = _prompt_bool("¿Incluye garantía extendida?", False)

    metrics = ProductMetrics(
        sku=sku,
        visits_per_day=visits,
        stock_units=stock,
        sales_per_day=sales,
        margin_percent=margin,
        lead_time_days=lead,
        financing_requested=financing,
        free_shipping=shipping,
        restricted_return=restricted,
        extended_warranty=warranty,
        base_price=base,
    )

    service = DynamicPricingService()
    props = service.explain_propositions(metrics)
    decision = service.evaluate_product(metrics)
    _print_result(service, sku, props, decision)
    return 0


def run_interactive(mode: str) -> int:
    if mode == "interview":
        return run_interview_mode()
    return run_metrics_mode()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Sistema experto de precios — taller CLIPS",
    )
    parser.add_argument(
        "--mode",
        choices=("interview", "metrics"),
        default="interview",
        help="interview: 12 preguntas sí/no; metrics: umbrales numéricos",
    )
    args = parser.parse_args()
    try:
        raise SystemExit(run_interactive(args.mode))
    except KeyboardInterrupt:
        print("\nCancelado.")
        raise SystemExit(130) from None
    except Exception as exc:  # noqa: BLE001 — CLI amigable
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
