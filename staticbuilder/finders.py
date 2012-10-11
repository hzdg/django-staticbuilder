from django.conf import settings
from django.contrib.staticfiles import utils
from django.contrib.staticfiles.finders import BaseStorageFinder
from .storage import BuiltFileStorage


class BuiltFileFinder(BaseStorageFinder):
    storage = BuiltFileStorage


class BuildableFileFinder(object):
    """
    Wraps a finder class in order to exclude files.

    """
    def __init__(self, finder, include_patterns=None):
        self.wrapped = finder
        self.include_patterns = include_patterns or settings.STATICBUILDER_INCLUDE_FILES

    def list(self, ignore_patterns):
        """
        Delegate the work of this method to the wrapped finder, but filter its
        results.

        """
        for path, storage in self.wrapped.list(ignore_patterns):
            if utils.matches_patterns(path, self.include_patterns):
                yield path, storage

    def __getattr__(self, name):
        """
        Proxy to the wrapped object.

        """
        return getattr(self.wrapped, name)
