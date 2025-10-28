"""
Lightweight keyword extractor (prefers nouns) with NLTK fallback
"""

import re
from collections import Counter
from typing import List


class KeywordExtractor:
    def __init__(self) -> None:
        self._nltk_ready = self._ensure_nltk()
        self._stopwords = self._load_stopwords()

    def extract_keywords(self, text: str, top_k: int = 3) -> List[str]:
        if not text:
            return []

        tokens = self._tokenize(text)
        if self._nltk_ready:
            try:
                import nltk

                tagged = nltk.pos_tag(tokens)
                candidates = [w.lower() for w, t in tagged if t.startswith("NN")]
            except Exception:
                candidates = [t.lower() for t in tokens]
        else:
            candidates = [t.lower() for t in tokens]

        words = [w for w in candidates if w.isalpha() and w not in self._stopwords and len(w) > 2]
        freq = Counter(words)
        ordered: List[str] = []
        for w, _ in freq.most_common():
            if w not in ordered:
                ordered.append(w)
            if len(ordered) >= top_k:
                break
        return ordered

    def _tokenize(self, text: str) -> List[str]:
        if self._nltk_ready:
            try:
                import nltk

                return nltk.word_tokenize(text)
            except Exception:
                pass
        return re.findall(r"\b\w+\b", text)

    def _ensure_nltk(self) -> bool:
        try:
            import nltk

            resources = [
                ("tokenizers/punkt", "punkt"),
                ("taggers/averaged_perceptron_tagger", "averaged_perceptron_tagger"),
                ("taggers/averaged_perceptron_tagger_eng", "averaged_perceptron_tagger_eng"),
                ("corpora/stopwords", "stopwords"),
            ]
            for path, name in resources:
                try:
                    nltk.data.find(path)
                except LookupError:
                    try:
                        nltk.download(name, quiet=True)
                    except Exception:
                        return False
            return True
        except Exception:
            return False

    def _load_stopwords(self) -> set:
        base = {
            "the","a","an","and","or","but","if","while","with","to","of","in","for","on","at","by","from","as","is","are","was","were","be","been","being","that","this","these","those","it","its","into","about","over","after","before","between","within","without","through","up","down","out","off","than","then","so","such","not","no","nor","too","very","can","could","should","would","will","may","might","must","do","does","did","doing","have","has","had"
        }
        if self._nltk_ready:
            try:
                from nltk.corpus import stopwords as sw

                return set(sw.words("english")).union(base)
            except Exception:
                return base
        return base


# Global instance
keyword_extractor = KeywordExtractor()
