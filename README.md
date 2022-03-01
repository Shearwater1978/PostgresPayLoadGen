# PostgresPayLoadGen


[![Build Status](https://app.travis-ci.com/Uglykoyote/PostgresPayLoadGen.svg?branch=master)](https://app.travis-ci.com/Uglykoyote/PostgresPayLoadGen)


Added python script to check connectivity to PostgresSQL db

```
 docker run -it -e DB_USER_NAME=pguser -e DB_USER_PASS=pgpass -e DB_USER_DB=pgbase -e DB_USER_PG_HOST=192.168.1.152 -e DB_USER_PG_PORT=5432 geninfo:latest
```
If env variables are not set - the script abnormally stops.

Palyload script generate fake Person records with next fields:

| Field name  | Value |
| ------------- | ------------- |
| uuid  | Unique uid for person  |
| fio  | First name + Surename + Last name  |
| phone  | Cellular number in the Russian format with code +7|
| age  | Age generated between 18 and 20 year (can be changed directly in python script)  |
| addr  | Address of leaving the fake person  |
| email  | Email  |


SQL script to create db person
```
CREATE TABLE person (
    uuid VARCHAR ( 36 ) NOT NULL,
    fio VARCHAR ( 50 ) NOT NULL,
    phone VARCHAR ( 18 ) NOT NULL,
    age INT NOT NULL,
    addr VARCHAR ( 75 ) NOT NULL,
    email VARCHAR ( 75 ) NOT NULL
);
```

Run db PostgreSQL in docker container
```
docker run --name postgres -e POSTGRES_PASSWORD=pgpass -e POSTGRES_USER=pguser -e POSTGRES_DB=person -d -p5432:5432 -v `pwd`/SQL/init_db/:/docker-entrypoint-initdb.d/ postgres
```

Get records from PostgreSQL
```
psql -U pguser -d person -h 0.0.0.0 < ./SQL/get_count_of_records.sql
```
