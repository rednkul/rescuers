import datetime

def date_next_attestation(date_attestation):
    next_attestation = datetime.date(date_attestation.year + 3, date_attestation.month, date_attestation.day)

    return next_attestation

def define_90d_before_atestation(next_attestation):

    day_trigger = next_attestation - datetime.timedelta(days=90)

