# The authoritative version is set by CI at build time:
#   - docker:  ARG APP_VERSION is baked into KOALIXCRM_VERSION (env) and
#              this file is overwritten inside the image (see docker/prod/*).
#   - PyPI:    .github/workflows/buildAndReleasePyPiPackage.yaml rewrites this
#              file from the pushed git tag before `python setup.py sdist`.
#   - release: .github/workflows/release.yml writes the release version
#              here in the release commit, and "vX.Y.Z-develop" (the next
#              development version) in the commit after it.
#
# The placeholder below is what local (non-CI) runs see. It is deliberately
# non-PEP 440 so it cannot be uploaded to PyPI by accident.
KOALIXCRM_VERSION = "vX.Y.Z-develop"
