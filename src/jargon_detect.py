from __future__ import annotations
from typing import Tuple
from nltk.corpus import stopwords
from .utils import is_rare, CUSTOM_MAP

STOP = set(stopwords.words('english'))

FOCUS_POS_PREFIXES = ("N", "V", "J", "R")  # nouns, verbs, adj, adv

def is_candidate_complex(token: str, pos_tag: str) -> bool:
    if not token.isalpha():
        return False
    if token.lower() in STOP:
        return False
    if not pos_tag or not pos_tag[0] in FOCUS_POS_PREFIXES:
        return False
    # If in custom map, treat as complex (simplifiable)
    if token.lower() in CUSTOM_MAP:
        return True
    # Otherwise, frequency-based rarity
    return is_rare(token)
