import os
import re

from setuptools import find_packages, setup


def _resolve_version() -> str:
    """Resolve the package version.

    Precedence:
      1. KOALIXCRM_VERSION env var — set by CI (see .github/workflows/*).
      2. koalixcrm/version.py — auto-written by CI before PyPI upload, or
         carries the 'vX.Y.Z-develop' fallback during local development.
    """
    env_value = os.environ.get("KOALIXCRM_VERSION")
    if env_value:
        raw = env_value
    else:
        from koalixcrm.version import KOALIXCRM_VERSION
        raw = KOALIXCRM_VERSION

    # Normalise a git-style tag (e.g. 'v1.15.0', 'v1.15.0-dev5') into a
    # PEP 440 version (e.g. '1.15.0', '1.15.0.dev5'). Leave already-PEP 440
    # strings untouched.
    raw = raw.lstrip("v")
    raw = re.sub(r"-dev(\d+)$", r".dev\1", raw)
    return raw


with open("README.md", "r", encoding="utf-8") as readme_file:
    long_description = readme_file.read()

setup(name='koalix-crm',
      version=_resolve_version(),
      description='koalixcrm is a tiny and easy to use Customer-Relationship-Management'
                  ' Software (CRM) including tiny and easy to use Accounting Software',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='http://github.com/scaphilo/koalixcrm',
      author='Aaron Riedener',
      author_email='aaron.riedener@gmail.com',
      license='BSD',
      packages=find_packages(exclude=["projectsettings", "documentation",
                                      "tests", "tests.*",
                                      "*.tests", "*.tests.*"]),
      install_requires=['Django==5.2.14',
                        'django-filebrowser==5.0.0',
                        'olefile==0.47',
                        'Pillow==12.3.0',
                        'psycopg2-binary==2.9.12',
                        'django-grappelli==4.0.4',
                        'djangorestframework==3.17.2',
                        'djangorestframework-xml==2.0.0',
                        'django-filter==26.1',
                        'drf-spectacular==0.30.0',
                        'pandas==2.2.3',
                        'matplotlib==3.11.1',
                        'PyJWT[crypto]>=2.8.0',
                        ],
      # Test-only dependencies — mirrors docker/requirements/test.txt.
      # Not installed for a plain `pip install koalix-crm`; opt in with
      # `pip install koalix-crm[test]`. The prod image never installs these.
      extras_require={
          "test": [
              'pytest>=8.0.0',
              'pytest-cov>=5.0.0',
              'pytest-django>=4.7.0',
              'codacy-coverage>=1.3.11',
              'selenium>=4.16.0',
              'factory_boy>=3.3.0',
              'pylint>=3.1.0',
          ],
      },
      zip_safe=False,
      classifiers=['Development Status :: 4 - Beta',
                   'Programming Language :: Python :: 3.11', ],
      python_requires='>=3.11',
      include_package_data=True,
)
