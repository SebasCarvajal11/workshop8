"""Entrevista interactiva sí/no para las 12 proposiciones del taller."""

from __future__ import annotations

from .propositions import INTERVIEW_QUESTIONS, PROPOSITION_CODES, PropositionMap


def _prompt_yes_no(question: str, default: bool = False) -> bool:
    hint = "s/n"
    default_hint = "s" if default else "n"
    while True:
        raw = input(f"{question} ({hint}) [{default_hint}]: ").strip().lower()
        if not raw:
            return default
        if raw in ("s", "si", "sí", "y", "yes", "1"):
            return True
        if raw in ("n", "no", "0"):
            return False
        print("  Responda s (sí) o n (no).")


def run_proposition_interview() -> PropositionMap:
    print("\n--- Entrevista del sistema experto (12 proposiciones) ---\n")
    props: PropositionMap = {}
    for code, question in INTERVIEW_QUESTIONS:
        props[code] = _prompt_yes_no(question)
    for code in PROPOSITION_CODES:
        props.setdefault(code, False)
    return props
