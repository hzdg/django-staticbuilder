from blessings import Terminal
from django.conf import settings
from django.contrib.staticfiles import storage as djstorage
from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.utils.encoding import smart_str
import os
from pipes import quote
import shutil
import subprocess
from ...storage import BuiltFileStorage
from ...utils import patched_settings, patched_finders


t = Terminal()


class Command(BaseCommand):
    """
    Collects all static files into ``STATICBUILDER_BUILD_ROOT``, and then executes
    the shell commands in ``STATICBUILDER_BUILD_COMMANDS``.

    """

    help = 'Build optimized versions of your static assets.'
    requires_model_validation = False

    def handle(self, *args, **options):

        self.verbosity = int(options.get('verbosity', '1'))

        build_dir = settings.STATICBUILDER_BUILD_ROOT
        if not build_dir:
            raise ImproperlyConfigured('STATICBUILDER_BUILD_ROOT must be set.')

        # Remove the old build directory and backup
        bkup_dir = '%s.bkup' % build_dir
        shutil.rmtree(build_dir, ignore_errors=True)
        shutil.rmtree(bkup_dir, ignore_errors=True)

        # Back up the last build
        try:
            os.rename(build_dir, bkup_dir)
        except OSError:
            pass

        # Copy the static assets to a the build directory.
        self.log(t.bold('Collecting static assets for building...'))
        self.call_command_func(self.collect_for_build, build_dir)

        # Run the build commands.
        build_commands = getattr(settings, 'STATICBUILDER_BUILD_COMMANDS', None) or []
        for command in build_commands:
            cmd = command.format(build_dir=quote(build_dir))
            self.shell(cmd)

    def call_command_func(self, func, *args, **kwargs):
        print t.bright_black
        try:
            result = func(*args, **kwargs)
        finally:
            print t.normal
        return result

    def shell(self, cmd):
        self.log(t.bold('Running command: ') + cmd)

        return_code = subprocess.call(cmd, shell=True)
        if return_code:
            raise Exception('Failed with error code %s' % return_code)

    def collect_for_build(self, build_dir):
        with patched_finders():
            with patched_settings(STATICBUILDER_COLLECT_BUILT=False):
                # Patch the static files storage used by collectstatic
                storage = BuiltFileStorage()
                old_storage = djstorage.staticfiles_storage
                djstorage.staticfiles_storage = storage

                try:
                    call_command('collectstatic',
                                 verbosity=self.verbosity - 1,
                                 interactive=False,
                                 ignore_patterns=settings.STATICBUILDER_EXCLUDE_FILES)
                finally:
                    djstorage.staticfiles_storage = old_storage

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
