FROM python:alpine

WORKDIR /app

RUN apk update && apk upgrade
RUN apk add --no-cache bash \
                       gcc \
                       python2-dev \
                       libc-dev \
    && rm -rf /var/cache/apk/*

RUN pip install twittertail

EXPOSE 9000

ENTRYPOINT ["twittertail", "-w", "-u"]