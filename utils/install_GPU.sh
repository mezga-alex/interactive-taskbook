#!/bin/bash
source .skyengGF/bin/activate
conda install -c anaconda cudatoolkit
pip install -U spacy[cuda100]

nvidia-smi
python check_gpu.py
