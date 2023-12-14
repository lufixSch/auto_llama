from auto_llama.exceptions import ModuleDependenciesMissing

try:
    from txtai.pipeline import Similarity
    from nltk.stem import WordNetLemmatizer
except ImportError:
    raise ModuleDependenciesMissing("nlp", "nlp")

class ModelsLoader:
    """ Shared source for NLP models to reduce VRAM usage """

    _lemmatizer: WordNetLemmatizer = None
    _similarity: Similarity = None

    @property
    def lemmatizer(self):
        """NLTK WordNetLemmatizer"""

        if not self._lemmatizer:
            self._lemmatizer = WordNetLemmatizer()

        return self._lemmatizer

    @property
    def similarity(self):
        """txtai similarity pipeline"""

        if not self._similarity:
            self._similarity = Similarity()

        return self._similarity

models = ModelsLoader()
""" Shared source for NLP models to reduce VRAM usage """