from __future__ import annotations
from typing import List
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

def bleu_score(reference: str, hypothesis: str) -> float:
    smoothie = SmoothingFunction().method1
    ref_tokens = reference.split()
    hyp_tokens = hypothesis.split()
    return sentence_bleu([ref_tokens], hyp_tokens, smoothing_function=smoothie)

def corpus_bleu(references: List[str], hypotheses: List[str]) -> float:
    scores = [bleu_score(r, h) for r, h in zip(references, hypotheses)]
    return sum(scores) / len(scores) if scores else 0.0
