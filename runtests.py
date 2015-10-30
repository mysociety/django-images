#!/usr/bin/env python

import sys
import django
from django.conf import settings

settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    ROOT_URLCONF='images.urls',
    INSTALLED_APPS=(
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'sorl.thumbnail',
        'images',
    )
)

if django.VERSION[:2] >= (1, 7):
    django.setup()

if django.VERSION[:2] >= (1, 8):
    from django.test.runner import DiscoverRunner
    test_runner = DiscoverRunner(verbosity=1)
else:
    from django.test.simple import DjangoTestSuiteRunner
    test_runner = DjangoTestSuiteRunner(verbosity=1)

failures = test_runner.run_tests(['images'])
if failures:
    sys.exit(failures)
