#!bin/bash

# Install requirements
pipenv install --dev
pipenv install

# Spacy model
python -m spacy download en_core_web_sm