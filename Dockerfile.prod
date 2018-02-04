FROM python:3.6

WORKDIR /app

# Intall dependencies
COPY /requirements/base_requirements.txt /app/

COPY . /app

RUN chmod +x /app/entrypoint.prod.sh
ENTRYPOINT ["/app/entrypoint.prod.sh"]

