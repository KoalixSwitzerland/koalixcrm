from setuptools import setup, find_packages

setup(name='koalix-crm',
      version='1.12.dev1',
      description='koalixcrm is a tiny and easy to use Customer-Relationship-Management Software (CRM) including tiny and easy to use Accounting Software',
      url='http://github.com/scaphilo/koalixcrm',
      author='Aaron Riedener',
      author_email='aaron.riedener@gmail.com',
      license='BSD',
      packages=find_packages(exclude=["projectsettings", "documentation"]),
      install_requires=['Django==1.11.4','django-filebrowser-no-grappelli==3.7.2',
                        'lxml>=3.8.0','olefile>=0.44','Pillow>=4.2.1',
                        'psycopg2>=2.7.3', 'pytz>=2017.2', 'dajngo-grappelli==2.10.1',],
      zip_safe=False,
      classifiers=['Development Status :: 4 - Beta','Programming Language :: Python :: 3.4',],
      python_requires='~=3.5',
      include_package_data=True,
)

