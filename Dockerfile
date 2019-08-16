# pull official base image
FROM python:3.7-alpine

# set work directory
WORKDIR /app

# set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /app
# install dependencies
RUN apk add --no-cache python3-dev \
    && pip3 install --upgrade pip

RUN \
 apk add  postgresql-libs && \
 apk add --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

RUN \ 
 export FLASK_APP="run.py" \
 export APP_SETTINGS="development" \
 export DATABASE_URL= user='mcogol@myswl-database', password='Masterabram1!', host='myswl-database.mysql.database.azure.com', port=3306, database='vas_assets' \
 export DATABASE_TEST_URL="dbname='medicare_tests' host='localhost' port='0.0.0.0' user='Mcogol' password='root'" \
 export SECRET_KEY="mcogol" \
 export FLASK_DEBUG=1

# copy project


EXPOSE 5000

ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:5000", "-w", "4", "run:app"]