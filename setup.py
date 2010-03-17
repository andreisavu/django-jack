from distutils.core import setup

setup(name='django-jack',
      version='0.1',
      description='Jack and the Beanstalkd. Webapp for basic work queue administration',
      long_description='''Basic beanstalkd work queue administration, allows one to:
  - put job on queue in a given tube
  - inspect job: view body and statistics
  - inspect burried jobs and kick all or individual
  - inspect delayed jobs
  - view what tubes are currently in use and stats
  - view queue statistics
      ''',
      author='Andrei Savu',
      url='http://github.com/andreisavu/django-jack',
      packages=['jack'],
      classifiers=['Development Status :: 4 - Beta',
          'Framework :: Django',
          ],
      )
