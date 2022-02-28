# PostgresPayLoadGen


[![Build Status](https://app.travis-ci.com/Uglykoyote/PostgresPayLoadGen.svg?branch=master)](https://app.travis-ci.com/Uglykoyote/PostgresPayLoadGen)


Added python script to check connectivity to PostgresSQL db

```
 docker run -it -e DB_USER_NAME=pguser -e DB_USER_PASS=pgpass -e DB_USER_DB=pgbase -e DB_USER_PG_HOST=192.168.1.152 -e DB_USER_PG_PORT=5432 geninfo:latest
```
If env variables are not set - the script abnormally stops.

Palyload script generate fake Person records with next fields:
| Field | Value |
|---------------|
| fio | First name + Surename + Last name |
| phone | in the Russian format with code +7 |
| age | Age generated between 18 and 20 year (can be changed directly in python script) |
| city | City in Russia |
| addr | Address of leaving fake person |
| inn | Russian tax number |


DB Person
```
CREATE TABLE person (
    fio VARCHAR ( 50 ) NOT NULL,
    phone VARCHAR ( 18 ) NOT NULL,
    age INT NOT NULL,
    city VARCHAR ( 50 ) NOT NULL,
    address VARCHAR ( 75 ) NOT NULL,
    inn INT
);
```
