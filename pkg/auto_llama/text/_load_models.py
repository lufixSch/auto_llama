from auto_llama import exceptions, ModelLoader

HAS_DEPENDENCIES = True

try:
    import spacy
except ImportError:
    HAS_DEPENDENCIES = False


def _load_spacy():
    try:
        nlp = spacy.load("en_core_web_lg")

        return nlp
    except OSError:
        raise exceptions.ModelMissing("spacy")


def _register_models():
    if HAS_DEPENDENCIES:
        ModelLoader.add("spacy", _load_spacy)
