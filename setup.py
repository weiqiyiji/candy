from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='candy',
      version=version,
      description="Rime dict updater",
      keywords='rime dict sogou',
      author='jiluo',
      author_email='weiqiyiji@gmail.com',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'scrapy',
          'chardet'
      ],
      entry_points={
          'console_scripts': [
              'sougou_conv=candy.conv:sougou_main'
          ]
      },
      )
