# Contribute guide

To install all dependencies (use `poetry-core>=1.2.0a2`):

```bash
poetry install --with dev,docs
```

To run checks:

```bash
poetry run pre-commit run --all-files
```

To run tests:

```bash
poetry run pytest
```
