from blessings import Terminal
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.utils.encoding import smart_str
from optparse import make_option
from pipes import quote
import subprocess


t = Terminal()


class Command(BaseCommand):
    """
    Executes the shell commands in ``STATICBUILDER_BUILD_COMMANDS``
    on all static files in ``STATICBUILDER_BUILD_ROOT``.

    """

    help = 'Build optimized versions of your static assets.'
    requires_model_validation = False
    option_list = BaseCommand.option_list + (
        make_option('--nocollect',
            action='store_false',
            dest='collect',
            default=True,
            help='Skip collecting static files for build'),
    )

    def handle(self, *args, **options):

        self.verbosity = int(options.get('verbosity', '1'))

        build_dir = settings.STATICBUILDER_BUILD_ROOT
        if not build_dir:
            raise ImproperlyConfigured('STATICBUILDER_BUILD_ROOT must be set.')

        # Optionally run collectforbuild first (runs by default).
        if options['collect']:
            call_command('collectforbuild',
                         verbosity=self.verbosity,
                         interactive=False)

        # Run the build commands.
        build_commands = getattr(settings, 'STATICBUILDER_BUILD_COMMANDS', None) or []
        for command in build_commands:
            cmd = command.format(build_dir=quote(build_dir))
            self.shell(cmd)

    def shell(self, cmd):
        self.log(t.bold('Running command: ') + cmd)

        return_code = subprocess.call(cmd, shell=True)
        if return_code:
            raise Exception('Failed with error code %s' % return_code)

    def log(self, msg, level=1):
        """
        Log helper; from Django's collectstatic command.
        """
        msg = smart_str(msg)
        if not msg.endswith("\n"):
            msg += "\n"
        if level > 1:
            msg = t.bright_black(msg)
        if self.verbosity >= level:
            self.stdout.write(msg)
