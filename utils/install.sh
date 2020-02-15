#!/bin/bash
python -m venv .skyengGF
source .skyengGF/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm

