"""Raíz del proyecto (repo o imagen Docker /app)."""

from __future__ import annotations

import os
from pathlib import Path

_CLIPS_RULES = ("clips", "pricing-rules.clp")


def get_project_root() -> Path:
    """Directorio con clips/, web/, assets/ (desarrollo, Docker o APP_ROOT)."""
    if env := os.environ.get("APP_ROOT"):
        return Path(env).resolve()

    cwd = Path.cwd()
    if _has_clips_rules(cwd):
        return cwd

    here = Path(__file__).resolve()
    for candidate in (here.parents[2], here.parents[3], here.parents[1]):
        if _has_clips_rules(candidate):
            return candidate

    return cwd


def _has_clips_rules(root: Path) -> bool:
    return (root.joinpath(*_CLIPS_RULES)).is_file()
