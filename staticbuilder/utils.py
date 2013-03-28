from contextlib import contextmanager
from django.conf import settings
from django.contrib.staticfiles import finders
from .finders import BuildableFileFinder


@contextmanager
def patched_finders():
    old_get_finders = finders.get_finders

    def new_get_finders():
        for f in old_get_finders():
            yield BuildableFileFinder(f)

    finders.get_finders = new_get_finders
    yield
    finders.get_finders = old_get_finders


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
