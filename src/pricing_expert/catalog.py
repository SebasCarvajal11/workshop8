from dataclasses import dataclass

from .catalog_media import image_url_for_sku
from .metrics import ProductMetrics


@dataclass(frozen=True)
class StoreProduct:
    sku: str
    name: str
    description: str
    category: str
    image_url: str
    base_price: float
    default_metrics: ProductMetrics


def build_catalog() -> list[StoreProduct]:
    return [
        StoreProduct(
            sku="SKU-LAP-01",
            name="Laptop Pro 14",
            description="Ultrabook para trabajo y estudio. Precio sensible a demanda e inventario.",
            category="Computación",
            image_url=image_url_for_sku("SKU-LAP-01"),
            base_price=1299.0,
            default_metrics=ProductMetrics(
                sku="SKU-LAP-01",
                visits_per_day=1800,
                stock_units=6,
                sales_per_day=42,
                margin_percent=22,
                lead_time_days=18,
                financing_requested=False,
                free_shipping=True,
                restricted_return=False,
                extended_warranty=False,
                base_price=1299.0,
            ),
        ),
        StoreProduct(
            sku="SKU-AUD-02",
            name="Audífonos NoiseCancel X",
            description="Audio premium con promociones cuando las ventas son bajas.",
            category="Audio",
            image_url=image_url_for_sku("SKU-AUD-02"),
            base_price=249.0,
            default_metrics=ProductMetrics(
                sku="SKU-AUD-02",
                visits_per_day=320,
                stock_units=85,
                sales_per_day=3,
                margin_percent=48,
                lead_time_days=7,
                financing_requested=False,
                free_shipping=True,
                restricted_return=False,
                extended_warranty=True,
                base_price=249.0,
            ),
        ),
        StoreProduct(
            sku="SKU-MON-03",
            name='Monitor 27" 4K',
            description="Pantalla profesional; política de devolución restringida en oferta.",
            category="Monitores",
            image_url=image_url_for_sku("SKU-MON-03"),
            base_price=459.0,
            default_metrics=ProductMetrics(
                sku="SKU-MON-03",
                visits_per_day=90,
                stock_units=40,
                sales_per_day=8,
                margin_percent=8,
                lead_time_days=12,
                financing_requested=True,
                free_shipping=True,
                restricted_return=True,
                extended_warranty=False,
                base_price=459.0,
            ),
        ),
        StoreProduct(
            sku="SKU-CHR-04",
            name="Silla ergonómica AirSeat",
            description="Mobiliario con lead time largo y picos de demanda estacionales.",
            category="Hogar",
            image_url=image_url_for_sku("SKU-CHR-04"),
            base_price=389.0,
            default_metrics=ProductMetrics(
                sku="SKU-CHR-04",
                visits_per_day=1100,
                stock_units=4,
                sales_per_day=55,
                margin_percent=35,
                lead_time_days=22,
                financing_requested=False,
                free_shipping=False,
                restricted_return=False,
                extended_warranty=False,
                base_price=389.0,
            ),
        ),
    ]


_CATALOG_BY_SKU = {p.sku: p for p in build_catalog()}


def get_product(sku: str) -> StoreProduct | None:
    return _CATALOG_BY_SKU.get(sku)


def list_products() -> list[StoreProduct]:
    return list(_CATALOG_BY_SKU.values())
