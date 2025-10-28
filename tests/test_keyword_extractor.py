import sys
from pathlib import Path

# Ensure project root on path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.lib.keyword_extractor import keyword_extractor


def test_keyword_extractor_basic():
    text = (
        "Cats and dogs play in gardens. Cats love gardens. Dogs chase cats in the garden."
    )
    kws = keyword_extractor.extract_keywords(text)
    assert isinstance(kws, list)
    assert 0 <= len(kws) <= 3
    for w in kws:
        assert isinstance(w, str)
        assert w.isalpha()

    # Expect at least one likely noun from the text
    assert any(w in kws for w in ["cats", "dogs", "gardens", "garden"]) 
