# Contributing

When contributing to this repository, please first discuss the change you wish to make via issue,
email, or any other method with the owners of this repository before making a change. 

Please note we have a code of conduct, please follow it in all your interactions with the project.

## Licensing of Contributions

This project is released under the BSD 3-Clause License (see [LICENSE](LICENSE)).

By submitting a contribution (for example, a pull request), you agree that:

- your contribution is licensed to the project and to all downstream users
  under the same BSD 3-Clause License; and
- you have the right to license it under those terms — for example, it is your
  own original work, or you otherwise hold the rights needed to submit it.

You keep the copyright to your contribution; this is a license grant, not a
transfer of ownership.

If a file you add or change carries a copyright header (for example, the header
block of a gettext `.po` file), please make it match the project's
[LICENSE](LICENSE) — `Copyright (c) <year> Aaron Riedener` — rather than
"koalix" or any other organisation name.

## Pull Request Process

1. Ensure any install or build dependencies are removed before the end of the layer when doing a 
   build.
2. Update the README.md with details of changes to the interface, this includes new environment 
   variables, exposed ports, useful file locations and container parameters.
3. Increase the version numbers in all version.py files to the new version that this
   Pull Request would represent. The versioning scheme (see next section)
4. Crate a Pull Request towards the "development" branch, ensure that your pull-request 
   has at least 80% test-coverage and the Pull Request does not show issues in Travis 
5. Once the Pull Request is reviewed it will be merged by one of the core developers

## Versioning scheme
- 1.2.0.dev1  - Development release
- 1.2.0a1     - Alpha Release
- 1.2.0b1     - Beta Release
- 1.2.0rc1    - Release Candidate
- 1.2.0       - Final Release
- 1.2.0.post1 - Post Release
