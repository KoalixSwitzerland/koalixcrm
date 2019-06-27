from setuptools import setup, find_packages
from koalixcrm.version import KOALIXCRM_VERSION

setup(name='koalix-crm',
      version=KOALIXCRM_VERSION,
      description='koalixcrm is a tiny and easy to use Customer-Relationship-Management '
                  'Software (CRM) including tiny and easy to use Accounting Software',
      url='http://github.com/scaphilo/koalixcrm',
      author='Aaron Riedener',
      author_email='aaron.riedener@gmail.com',
      license='BSD',
      packages=find_packages(exclude=["projectsettings", "documentation"]),
      install_requires=['Django==1.11.21',
                        'django-filebrowser==3.9.1',
                        'lxml>=3.8.0',
                        'olefile>=0.44',
                        'Pillow==4.2.1',
                        'psycopg2_binary>=2.7.5',
                        'pytz==2017.2',
                        'django-grappelli==2.10.1',
                        'djangorestframework>=3.9.1',
                        'markdown==2.6.11',
                        'django-filter==1.1.0',
                        'djangorestframework-xml==1.3.0'
                        ],
      zip_safe=False,
      classifiers=['Development Status :: 4 - Beta',
                   'Programming Language :: Python :: 3.5',
                   ],
      python_requires='~=3.5',
      include_package_data=True,
)
