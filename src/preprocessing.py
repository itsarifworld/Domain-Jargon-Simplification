from __future__ import annotations
import nltk
from typing import List, Tuple
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag, word_tokenize

# Try to ensure required NLTK data
def _ensure_nltk():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')
        try:
            nltk.download('punkt_tab')  # new in recent NLTK versions
        except Exception:
            pass
    try:
        nltk.data.find('taggers/averaged_perceptron_tagger')
    except LookupError:
        nltk.download('averaged_perceptron_tagger')
        try:
            nltk.download('averaged_perceptron_tagger_eng')
        except Exception:
            pass
    try:
        nltk.data.find('corpora/wordnet')
    except LookupError:
        nltk.download('wordnet')
        nltk.download('omw-1.4')
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords')

_ensure_nltk()

WN_LEMMA = WordNetLemmatizer()

def penn_to_wn(tag: str):
    if tag.startswith('J'):
        return wn.ADJ
    if tag.startswith('V'):
        return wn.VERB
    if tag.startswith('N'):
        return wn.NOUN
    if tag.startswith('R'):
        return wn.ADV
    return None

def preprocess_sentence(text: str):
    tokens = word_tokenize(text)
    tagged = pos_tag(tokens)
    lemmas = []
    for tok, tag in tagged:
        wn_pos = penn_to_wn(tag) or wn.NOUN
        lemma = WN_LEMMA.lemmatize(tok, wn_pos)
        lemmas.append((tok, tag, lemma, wn_pos))
    return lemmas  # list of tuples (token, pos_tag, lemma, wn_pos)
