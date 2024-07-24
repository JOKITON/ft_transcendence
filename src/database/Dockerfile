FROM postgres:alpine3.20

EXPOSE 5432

# Add schema creation script
COPY ./init_db.sh /docker-entrypoint-initdb.d/
RUN chmod +x /docker-entrypoint-initdb.d/init_db.sh

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=5 \
  CMD pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}
