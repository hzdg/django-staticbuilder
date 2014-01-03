#/usr/bin/env python
import codecs
import os
from setuptools import setup, find_packages


read = lambda filepath: codecs.open(filepath, 'r', 'utf-8').read()

def exec_file(filepath, globalz=None, localz=None):
    exec(read(filepath), globalz, localz)

# Load package meta from the pkgmeta module without loading the package.
pkgmeta = {}
exec_file(os.path.join(os.path.dirname(__file__), 'staticbuilder', 'pkgmeta.py'),
         pkgmeta)


setup(
    name=pkgmeta['__title__'],
    description='Optimize your static files.',
    long_description=read(os.path.join(os.path.dirname(__file__), 'README.rst')),
    version=pkgmeta['__version__'],
    author=pkgmeta['__author__'],
    author_email='m@tthewwithanm.com',
    url='http://github.com/hzdg/django-staticbuilder',
    download_url='http://github.com/hzdg/django-staticbuilder/tarball/master',
    packages=find_packages(),
    zip_safe=False,
    keywords=['javascript', 'css', 'compressor', 'requirejs'],
    include_package_data=True,
    tests_require=[
        'nose',
        'unittest2',
    ],
    install_requires=[
        'Django>=1.4',
        'blessings==1.5',
        'django-appconf>=0.5',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Utilities'
    ],
    setup_requires=[],
)
