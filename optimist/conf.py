from appconf import AppConf


class OptimistConf(AppConf):
    COMMANDS = []
    COLLECT_OPTIMIZED = False

    class Meta:
        required = [
            'OPTIMIZED_ROOT',
        ]
