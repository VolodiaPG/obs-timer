FROM python:3.9-alpine
LABEL author=volodia version=0.1

RUN apk add --update build-base \ 
 && apk --no-cache add curl \
 && rm -rf /var/cache/apk/*

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

RUN mkdir /app
COPY . /app
WORKDIR /app
RUN source $HOME/.poetry/env && poetry config virtualenvs.create false
RUN source $HOME/.poetry/env && poetry install --no-dev

EXPOSE 8000
ENTRYPOINT ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "--reload", "main:app"]