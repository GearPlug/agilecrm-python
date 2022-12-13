import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='agilecrm-python',
      version='0.1.3',
      description='API wrapper for Agile CRM written in Python',
      long_description=read('README.md'),
      url='https://github.com/GearPlug/agilecrm',
      author='Miguel Ferrer',
      author_email='ingferrermiguel@gmail.com',
      license='GPL',
      packages=['agilecrm'],
      install_requires=[
          'requests',
      ],
      zip_safe=False)
