from appconf import AppConf


class StaticBuilderConf(AppConf):
    BUILD_COMMANDS = []
    COLLECT_BUILT = True
    INCLUDE_FILES = ['*']
    EXCLUDE_FILES = ['CVS', '.*', '*~']

    class Meta:
        required = [
            'BUILD_ROOT',
        ]
