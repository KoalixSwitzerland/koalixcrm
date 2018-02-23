FROM python:3.6

RUN mkdir /code
WORKDIR /code

# Intall dependencies
COPY /requirements/development_requirements.txt /code/
COPY /requirements/base_requirements.txt /code/

RUN pip install -r development_requirements.txt
COPY . /code

RUN chmod +x /code/entrypoint.sh
ENTRYPOINT ["/code/entrypoint.sh"]

