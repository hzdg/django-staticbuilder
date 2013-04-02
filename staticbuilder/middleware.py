from django.conf import settings
from django.core.management import call_command
import os
import time
from .utils import get_buildable_file_finders


class BuildOnRequest(object):
    """
    Middleware for automatically building your static files as part of the
    request-response cycle. The build step will only be run if the request
    returns an HTML response and a static file is found that has been modified
    more recently than your build directory.

    This middleware is meant to ease development (so you never see a page with
    old static files, or missing them entirely). It shouldn't be used in
    production, and is automatically disabled when your ``DEBUG`` setting is
    ``False``.

    """

    def process_response(self, request, response):
        if (
                settings.STATICBUILDER_BUILDONREQUEST_MIDDLEWARE_ENABLED and
                response.status_code == 200 and
                response['content-type'].startswith('text/html')):

            if not os.path.exists(settings.STATICBUILDER_BUILD_ROOT):
                call_command('buildstatic')
                return response

            last_built_at = os.path.getmtime(settings.STATICBUILDER_BUILD_ROOT)

            # Check to see if any static files have been updated.
            for finder in get_buildable_file_finders():
                for path, storage in finder.list([]):
                    mtime = time.mktime(storage.modified_time(path).timetuple())
                    if mtime > last_built_at:
                        # If a file has been updated, short circuit and rebuild.
                        call_command('buildstatic')
                        return response

        return response
