#!/usr/bin/env python

import os
from distutils.core import setup

setup(
    name='Django-temporal-models',
    version='0.0.2',
    description='Implementation of supporting temporality in Django models',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    url='https://github.com/TyumenGortrans/django-temporal-models',
    author='TyumenGortrans',
    author_email='django.temporal.models@gmail.com',
    packages=['temporal', 'temporal.models'],
    license='MIT License',
    platforms='OS Independent',
    classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: Russian',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Framework :: Django',
          'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)