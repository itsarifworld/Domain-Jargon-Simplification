from __future__ import annotations
from typing import Optional
import contextlib

# Optional grammar check via language-tool-python (graceful fallback)
def maybe_grammar_fix(text: str) -> str:
    try:
        import language_tool_python  # may require Java; if not available, we skip
        tool = language_tool_python.LanguageTool('en-US')
        matches = tool.check(text)
        return language_tool_python.utils.correct(text, matches)
    except Exception:
        return text  # fallback: return as-is
