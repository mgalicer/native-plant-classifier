FROM python:3.6 as base 

FROM base as builder

COPY requirements.txt /
RUN pip install --trusted-host pypi.python.org -r requirements.txt

FROM base

COPY --from=builder /usr/local /usr/local
COPY . /app
WORKDIR /app

EXPOSE 80

CMD [ "gunicorn",  "wsgi:app" ]
