Building Static Files
---------------------

Sooner or later, you're going to need to add a build step to your Django apps;
whether it's because of Sass_, Less_, Coffee_, AMD_, or just to optimize your
PNGs and JPEGs. There are a few__ popular__ ways to do some of these things with
Django, but each has its own specific goals, and you can easily find your build
requirements outside of their scope. django-staticbuilder takes a different
approach by giving you a simple way to add a build step to your workflow, but
has absolutely no opinion about what that build step should be, making it easy
to take advantage of whatever build tools you want.

Check out the full documentation on readthedocs__.

The heart of the staticbuilder build step is the ``buildstatic`` management
command, and it is stupid simple. In fact, it only does two things: first, it
collects your static files into a build directory and, second, it runs some
shell commands. (Seriously, look at `the source`__. It delegates most of its
work to Django's ``collectstatic``. And that's A Good Thing.)

To get started, add ``staticbuilder`` to your ``INSTALLED_APPS``:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'staticbuilder',
    )

To specify the build directory, use the ``STATICBUILDER_BUILD_ROOT`` setting:

.. code-block:: python

    STATICBUILDER_BUILD_ROOT = os.path.join(os.path.dirname(__file__), 'static_built')

To specify a list of shell commands to run with the ``STATICBUILDER_BUILD_COMMANDS``
setting:

.. code-block:: python

    STATICBUILDER_BUILD_COMMANDS = [
        'coffee -c /path/to/build_dir',
        'uglifyjs /path/to/build_dir/a.js -c > /path/to/build_dir/a.js',
    ]

or (to keep things a little more tidy):

.. code-block:: python

    STATICBUILDER_BUILD_COMMANDS = ['./bin/mybuildscript']

Finally, you'll need to add a special finder to your ``STATICFILES_FINDERS``
list:

.. code-block:: python

    STATICFILES_FINDERS = (
        'staticbuilder.finders.BuiltFileFinder',

        # The default Django finders:
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )

This finder is important—it's how Django finds the built versions of your files
when you run ``collectstatic``.


Development
-----------

In order to ease development, this package includes a middleware class that will
automatically build your static files as part of the request-response cycle. In
order to use it, just add it to your ``MIDDLEWARE_CLASSES`` setting:

.. code-block:: python

    MIDDLEWARE_CLASSES = (
        ...
        'staticbuilder.middleware.BuildOnRequest',
    )

Now, whenever you access a view that returns an HTML response, staticbuilder
will check to see if your static files have changed since the last build. If
they have, it will trigger a new build. This way, your static files will always
be up-to-date.

In order to make sure your responses are delivered quickly when developing,
you'll probably want to have different ``STATICBUILDER_BUILD_COMMANDS`` when
``DEBUG`` is ``True``. (For example, you probably don't need to compress your
CSS and JS while developing.)

This middleware is automatically disabled when ``DEBUG`` is ``False``, so it
won't run in production.


Collecting Without Building
---------------------------

The ``buildstatic`` command is actually a two-step process: collecting static
files into a build directory, and running some shell commands. The first step is
actually another command: ``collectforbuild``. This command may be run by itself
in the event that you want to do a different set of build steps than what you
have configured (during a deployment, for example).

The ``buildstatic`` command accepts an optional ``--nocollect`` flag that will
skip the ``collectforbuild`` step altogether. Note that this means
``collectforbuild`` will need to have been run at some point prior to
``buildstatic --nocollect``.


.. _Sass: http://sass-lang.com/
.. _Less: http://lesscss.org/
.. _Coffee: http://coffeescript.org/
.. _AMD: http://requirejs.org/docs/whyamd.html
__ https://github.com/jezdez/django_compressor
__ https://github.com/cyberdelia/django-pipeline
__ http://django-staticbuilder.readthedocs.org
__ https://github.com/hzdg/django-staticbuilder/blob/master/staticbuilder/management/commands/buildstatic.py
