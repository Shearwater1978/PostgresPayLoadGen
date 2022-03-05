#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE TABLE person (
    	uuid VARCHAR ( 36 ) NOT NULL,
    	fio VARCHAR ( 50 ) NOT NULL,
    	phone VARCHAR ( 18 ) NOT NULL,
    	age INT NOT NULL,
    	addr VARCHAR ( 75 ) NOT NULL,
    	email VARCHAR ( 75 ) NOT NULL
    );

EOSQL
