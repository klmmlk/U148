FROM python:3.12-slim

RUN mkdir /app \
    && apt-get update \
    && apt-get -y install git cron \
    && apt-get clean && rm -rf /var/lib/apt/lists/* \

WORKDIR /app
COPY * /app/
COPY cronjob /etc/cron.d/cronjob
RUN pip install -r /app/requirements.txt \
    && chmod 0644 /etc/cron.d/cronjob

CMD ["cron","-f"]