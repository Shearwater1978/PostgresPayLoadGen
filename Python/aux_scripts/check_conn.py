import psycopg2
import os
import sys
from datetime import datetime


def curr_time():
    dt = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    return(dt)


def get_creds():
    if os.getenv('DB_USER_NAME'):
        if os.getenv('DB_USER_PASS'):
            if os.getenv('DB_USER_DB'):
                if os.getenv('DB_USER_PG_HOST'):
                    if os.getenv('DB_USER_PG_PORT'):
                        dbport = int(os.getenv('DB_USER_PG_PORT'))
                    else:
                        dbport = 5432
                    dbhost = os.getenv('DB_USER_PG_HOST')
                dbname = os.getenv('DB_USER_DB')
            dbpass = os.getenv('DB_USER_PASS')
        dbuser = os.getenv('DB_USER_NAME')
    else:
        print('%s -> Some env varibale is not set or undefined. Script aborted' % curr_time(), file = sys.stderr)
        raise SystemExit(1)
    return(dbname, dbuser, dbpass, dbhost, dbport)


def check_conn():
    dbname, dbuser, dbpass, dbhost, dbport = get_creds()
    # Connect to your postgres DB
    try:
        conn = psycopg2.connect(
            host=dbhost,
            database=dbname,
            user=dbuser,
            password=dbpass,
            port=dbport,
            connect_timeout=5
        )
    except Exception as e:
        print("%s -> Unable to connect to db server: %s" % (curr_time(), e), file = sys.stderr)
        raise SystemExit(1)
    # Open a cursor to perform database operations
    cur = conn.cursor()
    # Execute a query
    SQL = "select * from pg_stat_activity;"
    cur.execute(SQL)
    # Retrieve query results
    records = cur.fetchall()
    if records:
        print("%s -> Connection to PG is active." % curr_time(), file = sys.stdout)
    else:
        print("%s -> Unable to established connecttion to db server: %s" % (curr_time(), e), file = sys.stderr)
        raise SystemExit(1)


def main():
    check_conn()


if __name__ == '__main__':
    main()
