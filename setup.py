import os
from setuptools import setup, find_packages

setup(name='dinette',
      description='Dinette is a forum application in the spirit of PunBB.',
      keywords='django, forum',

      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
)
