# pydummy

[![Build Status - master](https://travis-ci.org/PedrosWits/pydummy.svg?branch=master)](https://travis-ci.org/PedrosWits/pydummy)

A dummy template so you can get started with your python project.

## Requirements

These modules should probably be available system-wide:

```
virtualenv
tox
```

## Usage

Download asset.

Edit:

- Names: module, functions, `setup.py`, `docs/config.py`
- Author data: `setup.py`, `docs/config.py`
- Dependencies: `requirements.txt`
- Version number: `dummy/__init__.py`, `setup.py`, `docs/config.py`
- license
- docs

Remember:

- Pushes to github will trigger travis-ci.
- To package/test locally just run: `tox`


## Opinions

- **packaging**: setup.py and tox
- **testing**: pytest and tox
- **docs**: sphinx
- **continuous integration**: travis-ci
