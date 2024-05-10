from collections import Counter
from heapq import nlargest
from string import punctuation

from auto_llama import ModelLoader, exceptions

HAS_DEPENDENCIES = True

try:
    from spacy.lang.en.stop_words import STOP_WORDS
    from spacy.language import Language
except ImportError:
    HAS_DEPENDENCIES = False


class Summarizer:
    """Summarize a given text using NLP"""

    def __init__(self, text: str):
        if not HAS_DEPENDENCIES:
            raise exceptions.ExtrasDependenciesMissing(self.__class__.__name__, "text")

        self._text = text

        nlp = ModelLoader.get("spacy", Language)
        self._doc = nlp(self._text)

    def word_freq(self) -> Counter:
        """
        Return a Counter object with the normalized frequency of each word in the text.

        Excludes stop words
        """

        return self._word_freq(self._doc)

    def len(self) -> int:
        """
        Return the length of the text in number of sentences
        """

        cnt = 0
        for _ in self._doc.sents:
            cnt += 1

        return cnt

    def _word_freq(self, doc: "Language") -> Counter:
        """
        Return a Counter object with the normalized frequency of each word in the text.

        Excludes stop words
        """

        named_entities = [ent for ent in doc.ents]
        words = [
            token.text for token in named_entities if token.text not in STOP_WORDS or token.text not in punctuation
        ]

        words = Counter(words)

        max_cnt = words.most_common(1)[0][1]
        for word in words.keys():
            words[word] = words[word] / max_cnt

        return words

    def summarize(self, max_len: int = 5, separator: str = " ") -> str:
        """
        Summarize the given text to the maximum length of max_len sentences
        """

        word_freq = self.word_freq()
        sent_strength = {}

        for sent in self._doc.sents:
            sent_strength[sent.text] = sum([word_freq[word] for word in sent if word.text in word_freq.keys()])

        return separator.join(nlargest(max_len, sent_strength, key=sent_strength.get))

    # TODO: Add sentence shortening/splitting
    # TODO: Add goal specific summarizing (for task, search queries, ...)
