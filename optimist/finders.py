from django.contrib.staticfiles.finders import BaseStorageFinder
from .storage import OptimizedFileStorage


class OptimizedFileFinder(BaseStorageFinder):
    storage = OptimizedFileStorage
