from mimesis import Address
from mimesis import Person
from mimesis.enums import Gender
from mimesis.builtins import RussiaSpecProvider
from mimesis import Generic
from mimesis.providers.base import BaseProvider
import json
# import requests
import socket
import random
# import threading
import os
import psycopg2
import gc
# import resource
import sys
import time

generic = Generic('ru')


class Man(BaseProvider):
    class Meta:
      name = "man_provider"


    def __init__(self, **kwargs):
      super(Man, self).__init__(**kwargs)


#     @staticmethod
#     def personel(gender):
#       person = Person('ru')
#       phone_number = person.telephone()
#       age = person.age(minimum=18, maximum=20)
#       city = Address('ru').city()
#       address = Address('ru').address()
#       full_name = person.full_name(gender=gender, reverse = True) + ' ' + RussiaSpecProvider().patronymic(gender=gender)
#       inn = RussiaSpecProvider().inn()
#       passport = RussiaSpecProvider().passport_series() + ' ' + str(RussiaSpecProvider().passport_number())
#       json_out = json.dumps({'fio': full_name, 'phone': phone_number, 'age': age, 'city': city, 'address': address, 'inn': inn}, ensure_ascii=False)
#       return(json_out)


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


def insert(persons):
    dbname, dbuser, dbpass, dbhost, dbport = get_creds()
    # Connect to your postgres DB
    conn = psycopg2.connect(
        host=dbhost,
        database=dbname,
        user=dbuser,
        password=dbpass,
        port=dbport
    )
    # conn.autocommit = True
    # print("Cursor opening. Sent to stdout", file = sys.stdout)
    cursor = conn.cursor()
    i = 0
    persons_item_count = len(persons)
    # print("Get pesron count in array. Sent to stdout", file = sys.stdout)
    while i < persons_item_count:
    # for person in load_json(persons):
      # Open a cursor to perform database operations
      # print("Read %s item from array. Sent to stdout" % i, file = sys.stdout)
      person = json.loads(persons[i])
      cursor.execute("INSERT INTO person (fio, phone, age, city, addr, inn) VALUES(%s, %s, %s, %s, %s, %s)", (person['fio'], person['phone'], person['age'], person['city'], person['address'], person['inn']))
      # conn.commit()
      # print("Cursor executed. Sent to stdout", file = sys.stdout)
      i += 1
    persons = {}
    # print("Array is set to null. Sent to stdout", file = sys.stdout)
    conn.commit()
    # print("Made commit. Sent to stdout", file = sys.stdout)
    cursor.close()
    # print("Cursor closed. Sent to stdout", file = sys.stdout)
    conn.close()
    # print("Connection closed. Sent to stdout", file = sys.stdout)
    gc.collect()
    # print("Garbage collector executed. Sent to stdout", file = sys.stdout)


def new_pers(gender):
  print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++", file = sys.stdout)
  print("Called new_pers", file = sys.stdout)
  try:
    person = Person(Locate.RU)
  except:
    pass
  # Try to handle error when generate fio
  try:
    fio = person.full_name(gender=gender, reverse = True) + ' ' + RussiaSpecProvider().patronymic(gender=gender)
  except:
    fio = 'Неуловимый Джон Малкович'
  # Try to handle error when generate phone
  try:
    phone = person.telephone()
  except:
    phone = '+7-(920)-818-98-47'
  # Try to handle error when generate age
  try:
    age = person.age(minimum=18, maximum=20)
  except:
    age = 99
  # Try to handle error when generate City
  try:
    city = Address('de').city()
  except:
    city = 'Обломовск'
  # Try to handle error when generate address
  try:
    address = Address('de').address()
  except:
    address = 'ул. Луиджи Никакущего 1037'
  # Try to handle error when generate inn
  try:
    inn = RussiaSpecProvider().inn()
  except:
    inn = '432040743790'

  pers = {
      'fio': fio,
      'phone': phone,
      'age': age,
      'city': city,
      'address': address,
      'inn': inn
    }

  print("call new_pers. Generated record %s" % pers, file = sys.stdout)
  return(json.dumps(pers, ensure_ascii=False))


def call_personel(gender):
  return(generic.man_provider.personel(gender))


def gen_pers_arr(i):
  out_array = []
  if random.randint(1, 4) % 2 == 0:
    gender = Gender.FEMALE
  else:
    gender = Gender.MALE
  for item in range(0, i):
    print("call new_pers. Retrieve %s item. Sent to stdout" % item, file = sys.stdout)
    new_person = new_pers(gender)
    print("call gen_pers_arr. new_person is: %s" % new_person, file = sys.stdout)
    try:
      out_array.append(new_person)
    except MemoryError as e:
      print("call gen_pers_arr. Exception. Wrong data: %s" % new_person, file = sys.stdout)
  return(out_array)


def main():
  if os.getenv('SEND_TO_CONSOLE'):
    SEND_TO_CONSOLE = os.getenv('SEND_TO_CONSOLE')
  else:
    SEND_TO_CONSOLE = False

  generic.add_provider(Man)

  if os.getenv('BEHAVIOR_MODEL'):
    if os.getenv('BEHAVIOR_MODEL') == "push":
      if os.getenv('SEND_TO_API') == "true":
        if os.getenv('API_ENDPOINT'):
          if isOpen("localhost", 18080):
            # push_to_api(persons)
            pass
          else:
            print('Endpoint is set but inaccessible. Termination work')
            raise SystemExit(1)
        else:
          print('Endpoint URL not exists. Please set it and try again. Termination work')
          raise SystemExit(1)
  else:
    print('Set mode to "pull" model.')

  if os.getenv('RANDOM_FACTOR'):
    RANDOM_FACTOR = os.getenv('RANDOM_FACTOR')
  else:
    RANDOM_FACTOR = 1

  # Check for cyclial mode
  if os.getenv('CYCLIAL_MODE'):
    CYCLIAL_MODE = os.getenv('CYCLIAL_MODE')
  else:
    CYCLIAL_MODE = False

  if os.getenv('PERSON_COUNT'):
    try:
      person_count = int(os.getenv('PERSON_COUNT'))
    except:
      print('PERSON_COUNT is set but value is not number. Used default value - 10')
      person_count = 10
  else:
      print('PERSON_COUNT not found as env varibale. Used default value - 10')
      person_count = 10

  if CYCLIAL_MODE == "True":
    print('Enable cyclic mode')
    while True:
      persons = gen_pers_arr(person_count)
      if SEND_TO_CONSOLE == "False":
        insert(persons)
        print("Insert another %s record(-s). Sent to stdout" % person_count, file = sys.stdout)
      else:
        print(persons)
      persons = {}
      time.sleep(0.5)
      gc.collect()
  else:
    persons = gen_pers_arr(person_count)
    if SEND_TO_CONSOLE == "False":
      insert(persons)
      print("Insert single pack of %s record(-s). Sent to stdout" % person_count, file = sys.stdout)
    else:
      print(persons)


if __name__ == '__main__':
  main()
