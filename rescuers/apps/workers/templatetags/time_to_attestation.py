import datetime

from django import template

register = template.Library()


@register.filter
def next_attestation(value):

    last_attestation = value

    next_attestation = datetime.date(last_attestation.year + 3, last_attestation.month, last_attestation.day)

    month_names = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября',
                   'ноября', 'декабря']


    return f'{next_attestation.day} {month_names[next_attestation.month - 1]} {next_attestation.year} г.'



def next_attestation_excel(value):

    last_attestation = value

    next_attestation = datetime.date(last_attestation.year + 3, last_attestation.month, last_attestation.day)




    return f'{"0" + str(next_attestation.day) if next_attestation.day < 10 else next_attestation.day}.{"0" + str(next_attestation.month) if next_attestation.month < 10 else next_attestation.month}.{next_attestation.year}'

@register.filter
def time_between_now_and_next_attestation(value):
    last_attestation = value
    next_attestation = datetime.date(last_attestation.year + 3, last_attestation.month, last_attestation.day)

    td = next_attestation - datetime.date.today()
    print(int(str(td).split()[0]))
    return int(str(td).split()[0]) <= 90

