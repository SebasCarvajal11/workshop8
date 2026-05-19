"""Imágenes del catálogo: archivos en product-images/ del proyecto."""

from __future__ import annotations

import shutil
import unicodedata
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PRODUCT_IMAGES_IMPORT_DIR = PROJECT_ROOT / "product-images"
PRODUCTS_DIR = PROJECT_ROOT / "assets" / "products"
PUBLIC_PRODUCTS_DIR = PROJECT_ROOT / "web" / "public" / "products"

_SKU_BASENAME: dict[str, str] = {
    "SKU-LAP-01": "sku-lap-01",
    "SKU-AUD-02": "sku-aud-02",
    "SKU-MON-03": "sku-mon-03",
    "SKU-CHR-04": "sku-chr-04",
}

_SKU_HINTS: list[tuple[tuple[str, ...], str]] = [
    (("audifon", "noisecancel", "auricular", "headphone"), "sku-aud-02"),
    (("silla", "ergonomic", "chair", "airseat"), "sku-chr-04"),
    (("laptop", "portatil", "ultrabook", "pro 14", "comput"), "sku-lap-01"),
    (("monitor", "pantalla", "4k", "27"), "sku-mon-03"),
]

_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".avif", ".gif", ".svg"}
# Orden de preferencia al resolver URL por SKU (formatos raster modernos primero).
_PREFERRED_EXT = (".avif", ".webp", ".png", ".jpg", ".jpeg", ".gif", ".svg")


def _norm(text: str) -> str:
    folded = unicodedata.normalize("NFD", text)
    return "".join(c for c in folded if unicodedata.category(c) != "Mn").lower()


def _target_base_for_filename(stem: str) -> str | None:
    """Devuelve el nombre base canónico (sku-…) según el nombre de archivo."""
    name = _norm(stem)
    for hints, base in _SKU_HINTS:
        if any(hint in name for hint in hints):
            return base
    return None


def sync_product_images() -> None:
    """Copia imágenes desde product-images/ → assets/products y web/public/products."""
    PRODUCTS_DIR.mkdir(parents=True, exist_ok=True)
    PUBLIC_PRODUCTS_DIR.mkdir(parents=True, exist_ok=True)

    if not PRODUCT_IMAGES_IMPORT_DIR.is_dir():
        return

    for path in PRODUCT_IMAGES_IMPORT_DIR.iterdir():
        if not path.is_file():
            continue
        ext = path.suffix.lower()
        if ext not in _IMAGE_EXTENSIONS:
            continue

        target_base = _target_base_for_filename(path.stem)
        if not target_base:
            continue

        dest_name = f"{target_base}{ext}"
        dest_assets = PRODUCTS_DIR / dest_name
        dest_public = PUBLIC_PRODUCTS_DIR / dest_name
        shutil.copy2(path, dest_assets)
        shutil.copy2(path, dest_public)


def image_url_for_sku(sku: str) -> str:
    sync_product_images()
    base = _SKU_BASENAME.get(sku)
    if not base:
        return "/products/sku-lap-01.svg"

    for folder in (PUBLIC_PRODUCTS_DIR, PRODUCTS_DIR):
        if not folder.is_dir():
            continue
        for ext in _PREFERRED_EXT:
            path = folder / f"{base}{ext}"
            if path.is_file():
                version = int(path.stat().st_mtime)
                return f"/products/{path.name}?v={version}"

    return f"/products/{base}.svg"
