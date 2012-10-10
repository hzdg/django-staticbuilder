from django.contrib.staticfiles.finders import BaseStorageFinder
from .storage import BuiltFileStorage


class BuiltFileFinder(BaseStorageFinder):
    storage = BuiltFileStorage
