from setuptools import setup

setup(name='manadex',
      version='0.1',
      description='Magic: The Gathering card collection management website',
      author='Adam A.G. Shamblin',
      author_email='adam.shamblin@tutanota.com',
      license='MIT',
      install_requires=[
          'tornado>=4',
          'motor>=0.5',
          'honcho>=0.6'
      ],
      test_suite='nose.collector',
      tests_require=['nose'])
