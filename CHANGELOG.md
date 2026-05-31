# CHANGELOG


## v1.2.1 (2026-05-31)

### Bug Fixes

- Brought the publish ymls inline with other project
  ([`abfe66b`](https://github.com/garrethcain/easy-hmac/commit/abfe66bebb4a61ec347626dde9d771fe3f380533))


## v1.2.0 (2026-05-31)

### Features

- Add python-semantic-release for automated PyPI publishing
  ([`01afcef`](https://github.com/garrethcain/easy-hmac/commit/01afcef2c9c5fbbecf2beff0c770ed6d856824b0))

- Configure semantic-release in pyproject.toml with conventional commit parser - Add GitHub Action
  workflow triggered on push to main - Auto-version bump, changelog generation, build, and PyPI
  publish via OIDC - Create CHANGELOG.md placeholder

fix

build


## v1.1.0 (2026-05-30)

### Features

- Add python-semantic-release for automated PyPI publishing
  ([`76545f0`](https://github.com/garrethcain/easy-hmac/commit/76545f05f362d76ea66fd0bf9000747348d30570))

- Configure semantic-release in pyproject.toml with conventional commit parser - Add GitHub Action
  workflow triggered on push to main - Auto-version bump, changelog generation, build, and PyPI
  publish via OIDC - Create CHANGELOG.md placeholder

fix

- Add python-semantic-release for automated PyPI publishing
  ([`a3aabc4`](https://github.com/garrethcain/easy-hmac/commit/a3aabc465d60cebbc727c07e71534afe094acdff))

- Configure semantic-release in pyproject.toml with conventional commit parser - Add GitHub Action
  workflow triggered on push to main - Auto-version bump, changelog generation, build, and PyPI
  publish via OIDC - Create CHANGELOG.md placeholder


## v1.0.0 (2026-05-31)

### Build System

- Added the cicd for GitHub Actions
  ([`21d715c`](https://github.com/garrethcain/easy-hmac/commit/21d715cd1e99ab48edddae8ec729d520d9b8bd03))

- Dependency
  ([`b63b720`](https://github.com/garrethcain/easy-hmac/commit/b63b720a48412e8f04491dc04193fdfd7d359eed))

- Updated ver
  ([`cdce517`](https://github.com/garrethcain/easy-hmac/commit/cdce5172d075275e14351a808059f93df45805f4))

### Chores

- Updated licence
  ([`e92257b`](https://github.com/garrethcain/easy-hmac/commit/e92257bdeed554a45223fb91efa3f8bd4b9c0477))

### Documentation

- Added a brief how-to
  ([`bfae3d8`](https://github.com/garrethcain/easy-hmac/commit/bfae3d834ec2ca2af2ea196370efbb3ab4f4a21f))

- Corrected some text
  ([`305b88b`](https://github.com/garrethcain/easy-hmac/commit/305b88be6c37f7f149d4892333b99e52379702f0))

- Typo
  ([`f1b51ad`](https://github.com/garrethcain/easy-hmac/commit/f1b51ad70d5067e0669ad81d0c4d7a8fa97986ea))

### Refactoring

- Migrate from pipenv to uv with modern project structure
  ([`7d041a3`](https://github.com/garrethcain/easy-hmac/commit/7d041a3502e555a84a508805fae401dda9b055a3))

- Replace Pipfile/setuptools with pyproject.toml (hatchling build backend) - Flatten nested
  easy_hmac/ directory to standard src/ layout - Replace black/flake8 with ruff in pre-commit hooks
  - Move tests to tests/, LICENSE to root - Remove .releaserc.yaml (will be replaced by GitHub
  Action) - Update README developer instructions
