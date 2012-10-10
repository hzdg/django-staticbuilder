from django.core.files.storage import FileSystemStorage
from django.conf import settings


class OptimizedFileStorage(FileSystemStorage):
    def __init__(self, location=None, base_url=None, *args, **kwargs):
        if location is None:
            location = settings.OPTIMIST_OPTIMIZED_ROOT
        if base_url is None:
            base_url = settings.STATIC_URL
        super(OptimizedFileStorage, self).__init__(location, base_url,
                                                   *args, **kwargs)

    def find(self, path, all=False):
        if settings.OPTIMIST_COLLECT_OPTIMIZED:
            return super(OptimizedFileStorage, self).find(path, all)
        else:
            return []
