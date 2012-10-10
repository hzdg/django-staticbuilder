from appconf import AppConf


class StaticBuilderConf(AppConf):
    BUILD_COMMANDS = []
    COLLECT_BUILT = False

    class Meta:
        required = [
            'BUILT_ROOT',
        ]
