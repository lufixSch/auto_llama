""" Download spaCy ressources"""

import subprocess as sp
from spacy.cli.download import download as spacy_download

if __name__ == "__main__":
    spacy_ressources = ["en_core_web_lg", "en_core_web_trf"]
    coreferee_ressources = ['en']

    for res in spacy_ressources:
        spacy_download(res)

    for res in coreferee_ressources:
        sp.run(f"python -m coreferee install {res}", shell=True)