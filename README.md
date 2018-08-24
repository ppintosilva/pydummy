# pydummy

A dummy template so you can get started with your python project.

## Requirements

These modules should probably be available system-wide:

```
virtualenv
tox
```

## Usage

Download asset and edit:

- Names: module, functions, `setup.py`
- Author data: `setup.py`
- Dependencies: `requirements.txt`
- Version number: `dummy/__init__.py`, `setup.py`
- license

Remember:

- Pushes to github will trigger travis-ci.
- To package/test locally just run: `tox`


## Opinions

- **packaging**: setup.py and tox
- **testing**: pytest and tox
- **docs**: sphinx
- **continuous integration**: travis-ci
