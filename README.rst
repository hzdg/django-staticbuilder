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


.. _Sass: http://sass-lang.com/
.. _Less: http://lesscss.org/
.. _Coffee: http://coffeescript.org/
.. _AMD: http://requirejs.org/docs/whyamd.html
__ https://github.com/jezdez/django_compressor
__ https://github.com/cyberdelia/django-pipeline
__ http://django-staticbuilder.readthedocs.org
__ https://github.com/hzdg/django-staticbuilder/blob/master/staticbuilder/management/commands/buildstatic.py
