FROM python:3.6 as base 

FROM base as builder

COPY requirements.txt /
RUN pip install --trusted-host pypi.python.org -r requirements.txt

FROM base

COPY --from=builder /install /usr/local
WORKDIR /app
COPY . /app

EXPOSE 80

CMD [ "gunicorn",  "wsgi:app" ]
