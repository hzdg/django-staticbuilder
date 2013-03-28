from appconf import AppConf
from django.conf import settings


class StaticBuilderConf(AppConf):
    BUILDONREQUEST_MIDDLEWARE_ENABLED = None
    BUILD_COMMANDS = []
    COLLECT_BUILT = True
    INCLUDE_FILES = ['*']
    EXCLUDE_FILES = ['CVS', '.*', '*~']

    def configure_buildonrequest_middleware_enabled(self, value):
        return settings.DEBUG if value is None else value

    class Meta:
        required = [
            'BUILD_ROOT',
        ]
