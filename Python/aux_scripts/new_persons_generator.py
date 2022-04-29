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
import time
import random
from faker import Faker


def curr_time():
    dt = datetime.now().strftime("%H:%M:%S.%f")[:-4]
    return(dt)


def generate_bulk(count, generator):
    if generator == 'mimesis':
        _ = Field(locale=Locale.RU)
        schema = Schema(schema=lambda: {
            "uuid": _("uuid"),
            "fio": _("full_name", gender=Gender.FEMALE, reverse = True) + ' ' + RussiaSpecProvider().patronymic(gender=Gender.FEMALE),
            "phone": _("person.telephone"),
            "age": _("person.age", minimum=18, maximum=118),
            "address": _("address.address"),
            "email": _("person.email", domains=["test.com"], key=str.lower)
        })
        res = schema.create(iterations=count)
    else:
        fake = Faker('ru_RU')
        res = [{
            "uuid": fake.uuid4(),
            "fio": fake.name(),
            "phone": fake.phone_number(),
            "age": random.randint(18, 118),
            "address": fake.address(),
            "email": fake.email()} for x in range(count)]
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
        print('%s -> Some env varibale is not set or undefined. Script aborted' % curr_time(), file = sys.stderr)
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
        print('%s -> Unable to connect to db server. Exiting' % curr_time(), file = sys.stdout)
        raise SystemExit(1)
    cursor = conn.cursor()
    i = 0
    person_counts = len(persons)
    conn.set_session(autocommit=True)
    while i < person_counts:
        person = persons[i]
        cursor.execute("INSERT INTO person (uuid, fio, phone, age, addr, email) VALUES(%s, %s, %s, %s, %s, %s)", (person['uuid'], person['fio'], person['phone'], person['age'], person['address'], person['email']))
        i += 1
    # conn.commit()
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
            print('%s -> PERSON_COUNT is set but value is not number. Used default value - 10' % curr_time(), file = sys.stdout)
            PERSON_COUNT = 10
    else:
        print('%s -> PERSON_COUNT not found as env varibale. Used default value - 10' % curr_time(), file = sys.stdout)
        PERSON_COUNT = 10
    if os.getenv('NAME_OF_GENERATOR'):
        NAME_OF_GENERATOR = os.getenv('NAME_OF_GENERATOR')
    else:
        NAME_OF_GENERATOR = 'mimesis'
    return(SEND_TO_CONSOLE, CYCLIAL_MODE, PERSON_COUNT, NAME_OF_GENERATOR)


def actions(SEND_TO_CONSOLE, CYCLIAL_MODE, PERSON_COUNT, NAME_OF_GENERATOR):
    if CYCLIAL_MODE == "True":
        if os.getenv('RANDOM_FACTOR'):
            RANDOM_FACTOR = 1
        else:
            RANDOM_FACTOR = 0
        print('%s -> Enable cyclic mode' % curr_time(), file = sys.stdout)
        while True:
            start_time = datetime.now()
            # Implemented pause between two inserts to db
            if RANDOM_FACTOR == 1:
                sleep_time = round(random.randint(1, 500) / 100, 3)
            else:
                sleep_time = 0
            print('%s -> Goes to sleep for %s sec' % (curr_time(), sleep_time), file = sys.stdout)
            time.sleep(sleep_time)
            try:
                print('%s -> Start of generate another bulk of records.' % curr_time(), file = sys.stdout)
                persons = generate_bulk(PERSON_COUNT, NAME_OF_GENERATOR)
                print('%s -> End of generate another bulk of records.' % curr_time(), file = sys.stdout)
            except Exception as e:
                print('%s -> Unable to retrieve another bulk of records. Error: %s' % (curr_time(), e), file = sys.stderr)
            done_time = datetime.now()
            duration = done_time - start_time
            duration_in_s = duration.total_seconds()
            print('%s -> Pack of %s record(-s) generated within %s seconds' % (curr_time(), PERSON_COUNT, duration_in_s), file = sys.stdout)
            if SEND_TO_CONSOLE == "False":
                start_time = datetime.now()
                try:
                    print('%s -> Try to insert records into db' % (curr_time()), file = sys.stdout)
                    insert(persons)
                    print('%s -> Records are inserted' % curr_time(), file = sys.stdout)
                    persons = {}
                except Exception as e:
                    print('%s -> Unable to insert another bulk of records. Error: %s' % (curr_time(), e), file = sys.stderr)
                done_time = datetime.now()
                duration = done_time - start_time
                duration_in_s = duration.total_seconds()
                print('%s -> Inserted pack of record(-s) within %s seconds' % (curr_time(), duration_in_s), file = sys.stdout)
            else:
                print('%s -> Output record(-s)' % curr_time(), file = sys.stdout)
                print(persons)
    else:
        if SEND_TO_CONSOLE == "False":
            insert(persons)
            print('%s -> Insert single pack of record(-s)' % curr_time(), file = sys.stdout)
        else:
            persons = generate_bulk(PERSON_COUNT, NAME_OF_GENERATOR)
            print('%s -> Output record(-s)' % curr_time(), file = sys.stdout)
            print(persons)


def main():
    SEND_TO_CONSOLE, CYCLIAL_MODE, PERSON_COUNT, NAME_OF_GENERATOR = read_env()
    print('%s -> Start work' % curr_time(), file = sys.stdout)
    print('%s -> Selected generator: %s' % (curr_time(), NAME_OF_GENERATOR), file = sys.stderr)
    try:
        print('%s -> Run main function' % curr_time(), file = sys.stdout)
        actions(SEND_TO_CONSOLE, CYCLIAL_MODE, PERSON_COUNT, NAME_OF_GENERATOR)
    except Exception as e:
        print('%s -> Unable to execute Actions. Error: %s' % (curr_time(), e), file = sys.stdout)


if __name__ == '__main__':
    main()
