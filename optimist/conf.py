from appconf import AppConf


class OptimistConf(AppConf):
    COMMANDS = []
    COLLECT_OPTIMIZED = False
    FILES = ['*.css', '*.js']

    class Meta:
        required = [
            'OPTIMIZED_ROOT',
        ]
