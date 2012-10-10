from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.staticfiles.storage import StaticFilesStorage
from django.utils.encoding import smart_str
import os
from pipes import quote
import shutil
import subprocess
from ...utils import patched_settings


class Command(BaseCommand):
    help = 'Build optimized versions of your static assets.'

    def handle(self, *args, **options):

        self.verbosity = int(options.get('verbosity', '1'))

        target_dir = settings.STATICBUILDER_BUILT_ROOT

        # Remove the old build directory and backup
        build_dir = '%s.build' % target_dir
        bkup_dir = '%s.bkup' % target_dir
        shutil.rmtree(build_dir, ignore_errors=True)
        shutil.rmtree(bkup_dir, ignore_errors=True)

        # Back up the last build
        try:
            os.rename(target_dir, bkup_dir)
        except OSError:
            pass

        # Create the static build directory.
        os.makedirs(build_dir)

        # Recreate the target directory so that Django doesn't complain that
        # it doesn't exist (if it's in STATICFILES_DIRS)
        os.makedirs(target_dir)

        # Copy the static assets to a temporary directory in order to build.
        # We don't use BUILT_ROOT because Django doesn't allow you to collect
        # static files into a directory that's in STATICFILES_DIRS
        self.log('Collecting static assets for building...', 1)
        with patched_settings(STATIC_ROOT=build_dir,
                              STATIC_FILES_STORAGE=StaticFilesStorage):
            call_command('collectstatic',
                         verbosity=0,
                         interactive=False,
                         ignore_patterns=['CVS', '.*', '*~'])

        # Run the build commands.
        build_commands = getattr(settings, 'STATICBUILDER_BUILD_COMMANDS', None) or []
        for command in build_commands:
            # cmd = 'cd %s && %s' % (quote(tmpdir),
                                   # command.format(build_dir=quote(tmpdir)))
            cmd = command.format(build_dir=quote(build_dir))
            self.log('Running command: %s' % cmd, 1)
            p = subprocess.Popen([cmd], stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, shell=True)
            stdout, stderr = p.communicate()

            if stderr:
                raise Exception(stderr)

        # Move the new build directory
        shutil.rmtree(target_dir)
        os.rename(build_dir, target_dir)

    def log(self, msg, level=2):
        """
        Log helper; from Django's collectstatic command.
        """
        msg = smart_str(msg)
        if not msg.endswith("\n"):
            msg += "\n"
        if self.verbosity >= level:
            self.stdout.write(msg)
