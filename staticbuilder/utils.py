from contextlib import contextmanager
from django.conf import settings
from django.contrib.staticfiles import finders
from .finders import BuildableFileFinder


def get_buildable_file_finders():
    with patched_settings(STATICBUILDER_COLLECT_BUILT=False):
        for f in finders.get_finders():
            yield BuildableFileFinder(f)


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
