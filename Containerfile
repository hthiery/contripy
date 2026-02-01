FROM python:3.14-slim

COPY . /app
WORKDIR /app

RUN pip install .

CMD ["contripy"]