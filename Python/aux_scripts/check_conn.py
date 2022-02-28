import psycopg2
import os


def get_creds():
    if os.getenv('DB_USER_NAME'):
        if os.getenv('DB_USER_PASS'):
            if os.getenv('DB_USER_DB'):
                if os.getenv('DB_USER_PG_HOST'):
                    if os.getenv('DB_USER_PG_PORT'):
                        dbport = os.getenv('DB_USER_PG_PORT')
                    else:
                        dbport = "5432"
                    dbhost = os.getenv('DB_USER_PG_HOST')
                dbname = os.getenv('DB_USER_DB')
            dbpass = os.getenv('DB_USER_PASS')            
        dbuser = os.getenv('DB_USER_NAME')
    else:
        print('Some env varibale is not set or undefined. Script aborted')
        raise SystemExit(1)
    return(dbname, dbuser, dbpass, dbhost, dbport)


def check_conn():
    dbname,dbuser,dbpass,dbhost,dbport= get_creds()
    # Connect to your postgres DB
    conn = psycopg2.connect(
        host=dbhost,
        database=dbname,
        user=dbuser,
        password=dbpass,
        port=dbport
    )
    # Open a cursor to perform database operations
    cur = conn.cursor()
    # Execute a query
    SQL = "select * from pg_stat_activity;"
    cur.execute(SQL)
    # Retrieve query results
    records = cur.fetchall()
    if records:
        print("Connection to PG is active.")
    else:
        print("Unable to established connection to PG. Script aborted")
        raise SystemExit(1)

def main():
    check_conn()

if __name__ == '__main__':
      main()