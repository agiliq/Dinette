import os
from distutils.core import setup
from setuptools import find_packages

overview = open(os.path.join(os.path.dirname(__file__), 'docs/overview.txt'))
data = overview.read()
overview.close()

setup(
    name='dinette',
    description='Dinette is a forum application in the spirit of PunBB.',
    keywords='django, forum',
    packages=find_packages(exclude=["forum", "forum.*"]),
    include_package_data=True,
    version="1.2a",
    author="Agiliq Solutions",
    author_email="hello@agiliq.com",
    long_description= data,
    classifiers = ['Development Status :: 4 - Beta',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: GNU General Public License (GPL)',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Internet :: WWW/HTTP',
                   'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
                   'Topic :: Internet :: WWW/HTTP :: WSGI',
                   'Topic :: Software Development :: Libraries :: Application Frameworks',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                   ],
    url="http://www.agiliq.com/",
    license="GPL",
    platforms=["all"],
)
