from __future__ import annotations
from typing import List, Tuple, Optional
from nltk.corpus import wordnet as wn
from .utils import CUSTOM_MAP, simpler_choice, capitalize_like, apply_phrase_rules

def wordnet_candidates(lemma: str, wn_pos) -> List[str]:
    out = set()
    for syn in wn.synsets(lemma, pos=wn_pos):
        for l in syn.lemmas():
            name = l.name().replace('_', ' ')
            if name.isascii():
                out.add(name)
    return list(out)

def simplify_token(original: str, lemma: str, wn_pos) -> Optional[str]:
    low = original.lower()
    # 1) Custom map first (high precision)
    if low in CUSTOM_MAP:
        return capitalize_like(original, CUSTOM_MAP[low])
    # 2) WordNet candidates ranked by simplicity
    cands = wordnet_candidates(lemma, wn_pos)
    if cands:
        choice = simpler_choice(cands, original)
        if choice:
            return capitalize_like(original, choice)
    return None  # keep original

def phrase_then_word_level(text: str, tagged_lemmas: List[Tuple[str, str, str, str]]) -> str:
    # 1) Phrase-level rules
    text = apply_phrase_rules(text)

    # 2) Word-level
    out_tokens: List[str] = []
    for tok, tag, lemma, wn_pos in tagged_lemmas:
        repl = simplify_token(tok, lemma, wn_pos)
        out_tokens.append(repl if repl else tok)

    # Simple detokenization
    sent = "".join(
        [ ("" if i>0 and (t in ",.;:!?')\"]" ) else (" " if i>0 else "")) + t
          for i, t in enumerate(out_tokens) ]
    )
    # Fix opening punctuation spacing
    sent = sent.replace(" (", "(").replace(" [", "[")
    # Capitalize first character if needed
    return sent[0].upper() + sent[1:] if sent else sent
