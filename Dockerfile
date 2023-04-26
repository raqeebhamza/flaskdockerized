FROM python:3.9-alpine

RUN apk add --no-cache --virtual .build-deps g++ python3-dev libffi-dev openssl-dev && \
    apk add --no-cache --update python3 && \
    pip3 install --upgrade pip setuptools
RUN pip3 install pendulum service_identity
RUN mkdir /app
WORKDIR /app
COPY app/requirements.txt /app/requirements.txt
RUN pip install PyMySQL
RUN pip install -r requirements.txt
COPY app /app

ENTRYPOINT ["python"]
CMD ["app.py"]