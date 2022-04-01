# syntax=docker.dockerfile:1

FROM python:3.10.2

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "extract.py" ]
