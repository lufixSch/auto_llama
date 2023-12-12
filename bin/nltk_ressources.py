""" Download nltk ressources """

import nltk

if __name__ == "__main__":
    ressources = ["averaged_perceptron_tagger", "wordnet", "punkt"]

    # downloading nltk ressources
    for r in ressources:
        nltk.download(r)
