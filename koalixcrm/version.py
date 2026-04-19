# The authoritative version is set by CI at build time:
#   - docker:  ARG APP_VERSION is baked into KOALIXCRM_VERSION (env) and
#              this file is overwritten inside the image (see docker/prod/*).
#   - PyPI:    .github/workflows/buildAndReleasePyPiPackage.yaml rewrites this
#              file from the pushed git tag before `python setup.py sdist`.
#
# The placeholder below is what local (non-CI) runs see. It is deliberately
# non-PEP 440 so it cannot be uploaded to PyPI by accident.
KOALIXCRM_VERSION = "vX.Y.Z-develop"
