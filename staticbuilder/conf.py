from appconf import AppConf


class StaticBuilderConf(AppConf):
    BUILD_COMMANDS = []
    COLLECT_BUILT = False
    BUILDABLE_FILES = ['*.css', '*.js']

    class Meta:
        required = [
            'BUILT_ROOT',
        ]
