FROM python:3.7

COPY ./nlp /nlp
COPY ./server /server

# Install requirements
RUN pip install -r ./server/requirements.txt

# Spacy model
RUN python -m spacy download en_core_web_sm

CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8500"]
