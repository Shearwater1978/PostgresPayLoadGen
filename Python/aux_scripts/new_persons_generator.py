from mimesis.enums import Gender
from mimesis.locales import Locale
from mimesis.schema import Field, Schema
from mimesis.builtins import RussiaSpecProvider
from mimesis import Address
import os
import sys
import psycopg2
import json
from datetime import datetime


def generate_bulk(count):
    _ = Field(locale=Locale.RU)
    schema = Schema(schema=lambda: {
        "uuid": _("uuid"),
        "fio": _("full_name", gender=Gender.FEMALE, reverse = True) + ' ' + RussiaSpecProvider().patronymic(gender=Gender.FEMALE),
        "phone": _("person.telephone"),
        "age": _("person.age", minimum=18, maximum=65),
        "address": _("address.address"),
        "email": _("person.email", domains=["test.com"], key=str.lower)
    })
    res = schema.create(iterations=count)
    return(res)


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
        print('Some env varibale is not set or undefined. Script aborted', file = sys.stdout)
        raise SystemExit(1)
    return(dbname, dbuser, dbpass, dbhost, dbport)


def insert(persons):
    dbname, dbuser, dbpass, dbhost, dbport = get_creds()
    try:
        conn = psycopg2.connect(
            host=dbhost,
            database=dbname,
            user=dbuser,
            password=dbpass,
            port=dbport,
            connect_timeout=5
        )
    except:
        print('Unable to connect to db server. Exiting', file = sys.stdout)
        raise SystemExit(1)
    cursor = conn.cursor()
    i = 0
    person_counts = len(persons)
    while i < person_counts:
        person = persons[i]
        cursor.execute("INSERT INTO person (uuid, fio, phone, age, addr, email) VALUES(%s, %s, %s, %s, %s, %s)", (person['uuid'], person['fio'], person['phone'], person['age'], person['address'], person['email']))
        i += 1
    # for person in load_json(persons):
    #     cursor.execute("INSERT INTO person (fio, phone, age, city, addr, inn) VALUES(%s, %s, %s, %s, %s, %s)", (person['fio'], person['phone'], person['age'], person['city'], person['address'], person['inn']))
    conn.commit()
    cursor.close()
    conn.close()


def read_env():
    # Check for output to console
    if os.getenv('SEND_TO_CONSOLE'):
        SEND_TO_CONSOLE = os.getenv('SEND_TO_CONSOLE')
    else:
        SEND_TO_CONSOLE = False
    # Check for cyclial mode enabled
    if os.getenv('CYCLIAL_MODE'):
        CYCLIAL_MODE = os.getenv('CYCLIAL_MODE')
    else:
        CYCLIAL_MODE = False
    if os.getenv('PERSON_COUNT'):
        try:
            PERSON_COUNT = int(os.getenv('PERSON_COUNT'))
        except:
            print('PERSON_COUNT is set but value is not number. Used default value - 10', file = sys.stdout)
            PERSON_COUNT = 10
    else:
        print('PERSON_COUNT not found as env varibale. Used default value - 10', file = sys.stdout)
        PERSON_COUNT = 10
    return(SEND_TO_CONSOLE, CYCLIAL_MODE, PERSON_COUNT)


def actions(SEND_TO_CONSOLE, CYCLIAL_MODE, PERSON_COUNT):
    if CYCLIAL_MODE == "True":
        print('Enable cyclic mode', file = sys.stdout)
        while True:
            start_time = datetime.now()
            persons = generate_bulk(PERSON_COUNT)
            done_time = datetime.now()
            duration = done_time - start_time
            duration_in_s = duration.total_seconds()
            dt = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            print("%s -> Pack of %s record(-s) generated within %s seconds" % (dt, PERSON_COUNT, duration_in_s), file = sys.stdout)
            if SEND_TO_CONSOLE == "False":
                start_time = datetime.now()
                insert(persons)
                done_time = datetime.now()
                duration = done_time - start_time
                duration_in_s = duration.total_seconds()
                dt = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                print("%s -> Inserted pack of record(-s) within %s seconds" % (dt, duration_in_s), file = sys.stdout)
            else:
                dt = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                print("%s -> Output record(-s)"% dt, file = sys.stdout)
                print(persons)
    else:
        if SEND_TO_CONSOLE == "False":
            insert(persons)
            dt = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            print("%s -> Insert single pack of record(-s)" % dt, file = sys.stdout)
        else:
            persons = generate_bulk(PERSON_COUNT)
            dt = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            print("%s -> Output record(-s)"% dt, file = sys.stdout)
            print(persons)


def main():
    SEND_TO_CONSOLE, CYCLIAL_MODE, PERSON_COUNT = read_env()
    actions(SEND_TO_CONSOLE, CYCLIAL_MODE, PERSON_COUNT)


if __name__ == '__main__':
    main()
