# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Dockerfile                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jaizpuru <jaizpuru@student.42urduliz.co    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/09/14 23:02:29 by jaizpuru          #+#    #+#              #
#    Updated: 2024/09/16 17:30:49 by jaizpuru         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

FROM alpine:3.20

RUN apk add --no-cache curl tzdata shadow openssl netcat-openbsd zsh python3

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy the migration script
COPY run_migrations.sh run_migrations.sh

# Set execute permissions for the migration script
RUN chmod +x run_migrations.sh

COPY requirements.txt utils/requirements.txt

RUN python -m venv /opt/venv && source /opt/venv/bin/activate \
  && pip install --no-cache-dir -r utils/requirements.txt

ENV PATH="/opt/venv/bin:$PATH"

# CMD ["sleep", "infinity"]
CMD ["sh", "run_migrations.sh"]