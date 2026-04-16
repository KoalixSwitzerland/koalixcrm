from setuptools import setup, find_packages
from koalixcrm.version import KOALIXCRM_VERSION

with open("README.md", "r", encoding="utf-8") as readme_file:
    long_description = readme_file.read()

setup(name='koalix-crm',
      version=KOALIXCRM_VERSION,
      description='koalixcrm is a tiny and easy to use Customer-Relationship-Management'
                  ' Software (CRM) including tiny and easy to use Accounting Software',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='http://github.com/scaphilo/koalixcrm',
      author='Aaron Riedener',
      author_email='aaron.riedener@gmail.com',
      license='BSD',
      packages=find_packages(exclude=["projectsettings", "documentation"]),
      install_requires=['Django==5.2.13',
                        'django-filebrowser==4.0.3',
                        'lxml==5.4.0',
                        'olefile==0.46',
                        'Pillow==12.2.0',
                        'psycopg2-binary==2.9.11',
                        'django-grappelli==3.0.10',
                        'djangorestframework==3.16.0',
                        'djangorestframework-xml==2.0.0',
                        'markdown==3.8',
                        'django-filter==25.1',
                        'pandas==2.2.3',
                        'matplotlib==3.10.3',
                        'PyJWT[crypto]>=2.8.0',
                        ],
      zip_safe=False,
      classifiers=['Development Status :: 4 - Beta',
                   'Programming Language :: Python :: 3.11', ],
      python_requires='>=3.11',
      include_package_data=True,
)
