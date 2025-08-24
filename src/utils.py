from __future__ import annotations
import re
from typing import Optional, Iterable, Tuple, Dict, List
from wordfreq import zipf_frequency

# Small curated dictionary across domains (extend as you scale)
CUSTOM_MAP = {
    # Medicine
    "arrhythmia": "irregular heartbeat",
    "analgesics": "painkillers",
    "nociceptive": "pain",
    "antihypertensive": "blood pressure medicine",
    "metastasis": "spread of cancer",
    "pulmonary": "lung",
    "hypoglycemia": "low blood sugar",
    # Law
    "statute": "law",
    "encroachment": "intrusion",
    "alibi": "excuse",
    "forensic": "scientific",
    "adjudicate": "decide",
    "constitutional": "basic law",
    "proceedings": "case steps",
    "null and void": "cancelled",
    # Tech
    "algorithm": "method",
    "computational": "computer",
    "latency": "delay",
    "encryption": "coding",
    "confidentiality": "privacy",
    "vulnerabilities": "weaknesses",
    "cloud computing": "the cloud",
    "scalable": "easy to grow",
}

# Phrase-level rules (case-insensitive)
PHRASE_RULES = [
    (re.compile(r"\bnull\s+and\s+void\b", flags=re.I), "cancelled"),
    (re.compile(r"\brendered\s+null\s+and\s+void\b", flags=re.I), "cancelled"),
    (re.compile(r"\bstatute\s+prohibits\b", flags=re.I), "law forbids"),
]

def is_rare(word: str, lang: str = "en") -> bool:
    """Return True if the word is relatively uncommon (lower zipf score)."""
    if not word or not word.isalpha():
        return False
    score = zipf_frequency(word.lower(), lang)
    return score < 4.0  # ~ uncommon threshold

def simpler_choice(candidates: Iterable[str], original: str) -> Optional[str]:
    """Pick the simplest candidate: higher frequency, shorter length."""
    best = None
    best_key = None
    for cand in candidates:
        if not cand or cand.lower() == original.lower():
            continue
        f = zipf_frequency(cand.lower(), "en")
        key = (f, -len(cand))
        if best is None or key > best_key:
            best = cand
            best_key = key
    return best

def apply_phrase_rules(text: str) -> str:
    out = text
    for pattern, repl in PHRASE_RULES:
        out = pattern.sub(repl, out)
    return out

def capitalize_like(original: str, replacement: str) -> str:
    if original.istitle():
        return replacement.capitalize()
    if original.isupper():
        return replacement.upper()
    return replacement
