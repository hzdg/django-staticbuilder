Settings
========

.. currentmodule:: django.conf.settings


Build Settings
--------------

.. attribute:: STATICBUILDER_BUILD_COMMANDS

    :default: ``[]``

    A list of shell commands to be run by the ``buildstatic`` command.


.. attribute:: STATICBUILDER_BUILD_ROOT

    :default: ``None``

    The path of the directory in which static files should be collected for
    building. You must provide a value if using ``buildstatic`` (or
    ``staticbuilder.storage.BuiltFileStorage``)


.. attribute:: STATICBUILDER_INCLUDE_FILES

    :default: ``['*']``

    A list of patterns corresponding to files that should be collected for
    building.


.. attribute:: STATICBUILDER_EXCLUDE_FILES

    :default: ``['CVS', '.*', '*~']``

    A list of patterns corresponding to files that should be skipped when
    collecting for building.
