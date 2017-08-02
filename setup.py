from setuptools import setup, find_packages

setup(name='koalix-crm',
      version='1.11.dev2',
      description='koalixcrm is a tiny and easy to use Customer-Relationship-Management Software (CRM) including an also tiny and easy to use Accounting Software',
      url='http://github.com/scaphilo/koalixcrm',
      author='Aaron Riedener',
      author_email='aaron.riedener@gmail.com',
      license='BSD',
      packages=find_packages(),
      install_requires=['Django==1.11.4','django-filebrowser-no-grappelli==3.7.1','lxml>=3.8.0','olefile>=0.44','Pillow>=4.2.1','psycopg2>=2.7.3', 'pytz>=2017.2'],
      zip_safe=False,
      classifiers=['Development Status :: 4 - Beta','Programming Language :: Python :: 3.4',],
      python_requires='~=3.5',
      include_package_data=True,
)

