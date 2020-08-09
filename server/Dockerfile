FROM python:3.7

RUN pipenv shell

RUN sh server/setup.sh

COPY ./server /server

CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8500"]