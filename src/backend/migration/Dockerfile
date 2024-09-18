# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Dockerfile                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jaizpuru <jaizpuru@student.42urduliz.co    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/09/14 23:02:29 by jaizpuru          #+#    #+#              #
#    Updated: 2024/09/16 19:19:01 by jaizpuru         ###   ########.fr        #
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

RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

# CMD ["sleep", "infinity"]
CMD ["sh", "run_migrations.sh"]