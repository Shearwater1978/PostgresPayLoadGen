#!/usr/bin/env python

from mimesis import Address
from mimesis import Person
from mimesis.enums import Gender
from mimesis.builtins import RussiaSpecProvider
from mimesis import Generic
from mimesis.providers.base import BaseProvider
import json
import requests
import socket
import random
import threading
import os


generic = Generic('ru')


class Man(BaseProvider):
    class Meta:
      name = "man_provider"


    def __init__(self, **kwargs):
      super(Man, self).__init__(**kwargs)


    @staticmethod
    def personel(gender):
      person = Person('ru')   
      phone_number = person.telephone()
      age = person.age(minimum=18, maximum=20)
      city = Address('ru').city()
      address = Address('ru').address()
      full_name = person.full_name(gender=gender, reverse = True) + ' ' +  RussiaSpecProvider().patronymic(gender=gender)
      inn = RussiaSpecProvider().inn()
      passport = RussiaSpecProvider().passport_series() + ' ' + str(RussiaSpecProvider().passport_number())
      json_out = json.dumps({'fio': full_name, 'phone': phone_number, 'age': age, 'city': city, 'address': address, 'inn': inn}, ensure_ascii=False)
      return(json_out)


def isOpen(ip,port):
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   try:
      s.connect((ip, int(port)))
      s.shutdown(2)
      return True
   except:
      return False


def new_pers(gender):
  person = Person('ru')
  pers = {
    'fio': person.full_name(gender=gender, reverse = True) + ' ' +  RussiaSpecProvider().patronymic(gender=gender),
    'phone': person.telephone(),
    'age': person.age(minimum=18, maximum=20),
    'city': Address('ru').city(),
    'address': Address('ru').address(),
    'inn': RussiaSpecProvider().inn()
  }
  return(json.dumps(pers))


def call_personel(gender):
  return(generic.man_provider.personel(gender))


def checkOpenPort(ip, port):
  if isOpen(ip,port):
    print('Connection opened')
  else:
    print("Port is closed. Script aborted")
    raise SystemExit(0)


def gen_pers_arr(i):
  out_array = []
  if random.randint(1,4)%2 == 0:
    gender = Gender.FEMALE
  else:
    gender = Gender.MALE
  for item in range(0,i):
   out_array.append(new_pers(gender))
  return(out_array)   


def send_to_api(person):
  requests.post("http://localhost:18080/api/v1/records", data=person.encode('utf-8'))


def push_to_api(persons):
  threads = []
  for person in persons:
    threads.append(threading.Thread(send_to_api(person)))
  for thread in threads:
    thread.start()
  for thread in threads:
    thread.join()


def main():
  generic.add_provider(Man)
  if os.getenv('PERSON_COUNT'):
    try:
      person_count = int(os.getenv('PERSON_COUNT'))
    except:
      print('PERSON_COUNT is set but value is not number. Used default value - 10')
      person_count = 10
  persons = gen_pers_arr(person_count)
  if os.getenv('BEHAVIOR_MODEL'):
    if os.getenv('BEHAVIOR_MODEL') == "push":
      if os.getenv('SEND_TO_API') == "true":
        if os.getenv('API_ENDPOINT'):
          if isOpen("localhost",18080):
            push_to_api(persons)
          else:
            print('Endpoint is set but inaccessible. Termination work')
            raise SystemExit(1)
        else:
          print('Endpoint URL not exists. Please set it and try again. Termination work')
          raise SystemExit(1)
  else:
    print('Set mode to "pull" model.')
  print(persons)



if __name__ == '__main__':
  main()