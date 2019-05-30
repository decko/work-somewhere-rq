FROM alpine:3.9

LABEL maintainer André "decko" de Brito <brito.afa@gmail.com>

ENV PYTHONBUFFERED 1

COPY . /telephone/
WORKDIR /telephone/

RUN echo "@edge http://dl-cdn.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories && \
	apk update && \
	apk add --no-cache python3@edge python3-dev@edge libpq ca-certificates && \
        apk add --no-cache --virtual=build-dependencies  wget postgresql-dev gcc musl-dev linux-headers git zlib-dev && \
        pip3 install pipenv && \
        pipenv install --system --deploy --ignore-pipfile && \
        apk del build-dependencies && \
        adduser -D -s /bin/false -u 1000 nonroot && \
        chown -R nonroot: * && \
	python3 ./manage.py collectstatic --no-input && \
	ln -s /usr/bin/python3 /usr/bin/python

USER nonroot

EXPOSE 5500
