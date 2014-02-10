from django.core.exceptions import ImproperlyConfigured
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os


class BuiltFileStorage(FileSystemStorage):
    _wrapped = None

    def __init__(self, location=None, base_url=None, *args, **kwargs):
        if location is None:
            location = settings.STATICBUILDER_BUILD_ROOT
            if not location:
                raise ImproperlyConfigured('STATICBUILDER_BUILD_ROOT must be set.')
        if base_url is None:
            base_url = settings.STATIC_URL
        super(BuiltFileStorage, self).__init__(location, base_url,
                                               *args, **kwargs)

    def find(self, path, all=False):
        if settings.STATICBUILDER_COLLECT_BUILT:
            return super(BuiltFileStorage, self).find(path, all)
        else:
            return []

    def listdir(self, path):
        if settings.STATICBUILDER_COLLECT_BUILT:
            return super(BuiltFileStorage, self).listdir(path)
        else:
            return [], []

    def delete(self, name):
        try:
            super(BuiltFileStorage, self).delete(name)
        except OSError:
            name = self.path(name)
            if os.path.isdir(name):
                os.rmdir(name)
            else:
                raise
