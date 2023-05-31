FROM python:3.8-alpine

WORKDIR /app

RUN apk --update add gcc build-base freetype-dev openblas-dev postgresql-dev python3-dev musl-dev libpq-dev

RUN pip install psycopg2 flask pandas sqlalchemy

# COPY ./requirements.txt /app/requirements.txt
# RUN pip install -r requirements.txt

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait

COPY . /app

CMD /wait & python app.py