FROM python:alpine

COPY . /app

WORKDIR /app

RUN apk update && apk upgrade
RUN apk add --no-cache bash \
                       gcc \
                       python2-dev \
                       libc-dev \
    && rm -rf /var/cache/apk/*

RUN pip install -r requirements.txt

EXPOSE 9000

ENTRYPOINT ["python", "-u", "twittertail", "-w", "-u"]