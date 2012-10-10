from contextlib import contextmanager
from django.conf import settings


@contextmanager
def patched_settings(**kwargs):
    old = {}
    for k, v in kwargs.items():
        try:
            old[k] = getattr(settings, k)
        except AttributeError:
            pass
        setattr(settings, k, v)
    yield
    for k, v in old.items():
        setattr(settings, k, v)
