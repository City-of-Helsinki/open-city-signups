from django.utils import formats, timezone


def localize_datetime(dt):
    return formats.date_format(timezone.localtime(dt), 'DATETIME_FORMAT')
