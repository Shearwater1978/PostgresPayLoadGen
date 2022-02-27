# PostgresPayLoadGen


[![Build Status](https://app.travis-ci.com/Uglykoyote/PostgresPayLoadGen.svg?branch=master)](https://app.travis-ci.com/Uglykoyote/PostgresPayLoadGen)


Added python script to check connectivity to PostgresSQL db

```
 docker run -it -e DB_USER_NAME=pguser -e DB_USER_PASS=pgpass -e DB_USER_DB=pgbase -e DB_USER_PG_HOST=192.168.1.152 -e DB_USER_PG_PORT=5432 geninfo:latest
```
If env variables are not set - the script abnormally stops.