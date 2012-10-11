from appconf import AppConf


class StaticBuilderConf(AppConf):
    BUILD_COMMANDS = []
    COLLECT_BUILT = True
    INCLUDE_FILES = ['*']

    class Meta:
        required = [
            'BUILT_ROOT',
        ]
