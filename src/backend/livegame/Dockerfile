FROM alpine:3.20

RUN apk add --no-cache curl tzdata shadow openssl netcat-openbsd zsh python3 jq

RUN cp /usr/share/zoneinfo/Europe/Madrid /etc/localtime

WORKDIR /livegame

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY livegame .

RUN python -m venv /opt/venv && source /opt/venv/bin/activate \
  && pip install --no-cache-dir -r utils/requirements.txt

ENV PATH="/opt/venv/bin:$PATH"

CMD ["zsh", "utils/init.sh"]
