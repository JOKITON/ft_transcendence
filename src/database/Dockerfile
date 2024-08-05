FROM postgres:alpine3.20

EXPOSE 5432

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=5 \
  CMD pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}
