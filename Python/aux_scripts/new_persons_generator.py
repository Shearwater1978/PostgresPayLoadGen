from mimesis.enums import Gender
from mimesis.locales import Locale
from mimesis.schema import Field, Schema
from mimesis.builtins import RussiaSpecProvider
from mimesis import Address


def generate_bulk(count)
    _ = Field(locale=Locale.RU)
    schema = Schema(schema=lambda: {
        "uid": _("uuid"),
        "fio": _("full_name", gender=Gender.FEMALE, reverse = True) + ' ' + RussiaSpecProvider().patronymic(gender=Gender.FEMALE),
        "phone": _("person.telephone"),
        "age": _("person.age", minimum=18, maximum=65),
        "address": _("address.address"),
        "email": _("person.email", domains=["test.com"], key=str.lower)
    })
    res = schema.create(iterations=count)
    return(res)


def read_env():
    # Check for output to console
    if os.getenv('SEND_TO_CONSOLE'):
        SEND_TO_CONSOLE = os.getenv('SEND_TO_CONSOLE')
    else:
        SEND_TO_CONSOLE = False
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
    return(SEND_TO_CONSOLE, CYCLIAL_MODE, PERSON_COUNT)


def main:
    SEND_TO_CONSOLE, CYCLIAL_MODE, PERSON_COUNT = read_env()
    print('SEND_TO_CONSOLE:{} CYCLIAL_MODE:{} PERSON_COUNT{}'.format(SEND_TO_CONSOLE, CYCLIAL_MODE, PERSON_COUNT))
    generate_bulk(count)


if __name__ == '__main__':
    main()
