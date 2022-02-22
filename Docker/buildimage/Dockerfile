FROM alpine

COPY posgtresql.ini /opt/
COPY PostgresPayLoadGen /opt/

RUN apk add --no-cache iproute2 libc6-compat
RUN chmod +x /opt/PostgresPayLoadGen

ENTRYPOINT ["/opt/PostgresPayLoadGen"]
