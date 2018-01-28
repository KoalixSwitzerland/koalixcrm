FROM python:3.6

WORKDIR /app

# Intall dependencies
COPY /requirements/development_requirements.txt /app/
COPY /requirements/base_requirements.txt /app/

RUN pip install -r development_requirements.txt

COPY . /app

ENTRYPOINT ["./entrypoint.sh"]
