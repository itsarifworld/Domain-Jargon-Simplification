import argparse
import pandas as pd
from src.preprocessing import preprocess_sentence
from src.jargon_detect import is_candidate_complex
from src.simplifier import phrase_then_word_level
from src.reconstruct import maybe_grammar_fix
from src.evaluate import corpus_bleu

def simplify_sentence(text: str) -> str:
    tagged = preprocess_sentence(text)
    # We pass all tokens through simplifier; jargon_detect is used implicitly
    simplified = phrase_then_word_level(text, tagged)
    simplified = maybe_grammar_fix(simplified)
    return simplified

def run_infer(input_csv: str, output_csv: str):
    df = pd.read_csv(input_csv)
    if 'Original' not in df.columns:
        raise ValueError("Input CSV must have an 'Original' column.")
    df_out = pd.DataFrame({
        'Original': df['Original'],
        'Simplified': [simplify_sentence(s) for s in df['Original']]
    })
    df_out.to_csv(output_csv, index=False)
    print(f"Saved: {output_csv}")

def run_eval(dataset_csv: str):
    df = pd.read_csv(dataset_csv)
    assert set(['Original','Simplified']).issubset(df.columns), "dataset.csv must have Original,Simplified"
    preds = [simplify_sentence(s) for s in df['Original']]
    score = corpus_bleu(df['Simplified'].tolist(), preds)
    print(f"BLEU (mini) = {score:.4f}")

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', type=str, default='data/test.csv', help='Path to input CSV')
    ap.add_argument('--output', type=str, default='output/submission.csv', help='Path to output CSV')
    ap.add_argument('--evaluate', action='store_true', help='Evaluate on dataset.csv with BLEU')
    args = ap.parse_args()

    if args.evaluate:
        run_eval(args.input)
    else:
        run_infer(args.input, args.output)
