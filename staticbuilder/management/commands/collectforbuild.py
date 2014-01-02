from blessings import Terminal
from django.conf import settings
from django.contrib.staticfiles import finders, storage as djstorage
from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.utils.encoding import smart_str, smart_unicode
from optparse import make_option
import os
from ...storage import BuiltFileStorage
from ...utils import patched_settings, patched_finders


t = Terminal()


class Command(BaseCommand):
    """
    Collects all static files into ``STATICBUILDER_BUILD_ROOT``.

    """

    help = 'Collect your static assets for building.'
    requires_model_validation = False
    option_list = BaseCommand.option_list + (
        make_option('-c', '--clean',
                    action='store_true',
                    dest='clean',
                    default=False,
                    help='Remove artifacts from previous builds'),
    )

    def handle(self, *args, **options):
        self.clean = options['clean']
        self.verbosity = int(options.get('verbosity', '1'))

        build_dir = settings.STATICBUILDER_BUILD_ROOT
        if not build_dir:
            raise ImproperlyConfigured('STATICBUILDER_BUILD_ROOT must be set.')

        # Copy the static assets to a the build directory.
        self.log(t.bold('Collecting static assets for building...'))
        self.call_command_func(self.collect_for_build, build_dir)

    def call_command_func(self, func, *args, **kwargs):
        print(t.bright_black)
        try:
            result = func(*args, **kwargs)
        finally:
            print(t.normal)
        return result

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

                # Delete the files that have been removed.
                if self.clean:
                    self.clean_built(storage)

    def find_all(self, storage, dir=''):
        """
        Find all files in the specified directory, recursively.

        """
        all_dirs = set()
        all_files = set()
        with patched_settings(STATICBUILDER_COLLECT_BUILT=True):
            dirs, files = storage.listdir(dir)
            all_dirs.update(os.path.join(dir, d) for d in dirs)
            all_files.update(os.path.join(dir, f) for f in files)
            for d in dirs:
                nested_dirs, nested_files = self.find_all(storage, os.path.join(dir, d))
                all_dirs.update(nested_dirs)
                all_files.update(nested_files)
        return (all_dirs, all_files)

    def clean_built(self, storage):
        """
        Clear any static files that aren't from the apps.

        """
        build_dirs, built_files = self.find_all(storage)

        found_files = set()
        for finder in finders.get_finders():
            for path, s in finder.list([]):
                # Prefix the relative path if the source storage contains it
                if getattr(s, 'prefix', None):
                    prefixed_path = os.path.join(s.prefix, path)
                else:
                    prefixed_path = path

                found_files.add(prefixed_path)

        stale_files = built_files - found_files

        for fpath in stale_files:
            self.log(u"Deleting '%s'" % smart_unicode(fpath), level=1)
            storage.delete(fpath)

        found_dirs = set()
        for f in found_files:
            path = f
            while True:
                path = os.path.dirname(path)
                found_dirs.add(path)
                if not path:
                    break

        stale_dirs = set(build_dirs) - found_dirs

        for fpath in stale_dirs:
            try:
                storage.delete(fpath)
            except OSError:
                self.log(u"Couldn't remove empty directory '%s'" % smart_unicode(fpath), level=1)
            else:
                self.log(u"Deleted empty directory '%s'" % smart_unicode(fpath), level=1)

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
