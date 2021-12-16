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


@register.filter
def time_between_now_and_next_attestation(value):
    last_attestation = value
    next_attestation = datetime.date(last_attestation.year + 3, last_attestation.month, last_attestation.day)

    td = next_attestation - datetime.date.today()
    print(f'{value}--------------------{bool(int(str(td).split()[0]) <= 90)}')
    return int(str(td).split()[0]) <= 90

