from blessings import Terminal
from contextlib import contextmanager
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.staticfiles import finders
from django.contrib.staticfiles.storage import StaticFilesStorage
from django.utils.encoding import smart_str
import os
from pipes import quote
import shutil
import subprocess
from ...finders import OptimizableFileFinder
from ...utils import patched_settings


t = Terminal()


@contextmanager
def optimizable_files_finders():
    old_get_finders = finders.get_finders

    def new_get_finders():
        for f in old_get_finders():
            yield OptimizableFileFinder(f)

    finders.get_finders = new_get_finders
    yield
    finders.get_finders = old_get_finders


class Command(BaseCommand):
    help = 'Build optimized versions of your static assets.'

    def handle(self, *args, **options):

        self.verbosity = int(options.get('verbosity', '1'))

        build_dir = settings.OPTIMIST_OPTIMIZED_ROOT

        # Remove the old build directory and backup
        bkup_dir = '%s.bkup' % build_dir
        shutil.rmtree(build_dir, ignore_errors=True)
        shutil.rmtree(bkup_dir, ignore_errors=True)

        # Back up the last build
        try:
            os.rename(build_dir, bkup_dir)
        except OSError:
            pass

        # Create the static build directory.
        os.makedirs(build_dir)

        # Copy the static assets to the build directory.
        self.log(t.bold('Collecting static assets for building...'))
        self.call_command_func(self.collect_for_build, build_dir)

        # Run the build commands.
        commands = getattr(settings, 'OPTIMIST_COMMANDS', None) or []
        for command in commands:
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
        p = subprocess.Popen([cmd], stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, shell=True)
        stdout, stderr = p.communicate()

        if stdout:
            self.log(stdout, level=2)

        if stderr:
            raise Exception(stderr)

    def collect_for_build(self, build_dir):
        with optimizable_files_finders():
            with patched_settings(STATIC_ROOT=build_dir,
                                  STATIC_FILES_STORAGE=StaticFilesStorage,
                                  OPTIMIST_COLLECT_OPTIMIZED=False):
                call_command('collectstatic',
                              verbosity=self.verbosity - 1,
                              interactive=False,
                              ignore_patterns=['CVS', '.*', '*~'])

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
