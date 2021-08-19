from pathlib import Path

import toml

import table2sql


def test_versions_are_in_sync():
    """
    Checks if the pyproject.toml and package.__init__.py __version__ are in sync.

    Code posted by @ttamg and taken from [here](https://github.com/python-poetry/poetry/issues/144#issuecomment-877835259)
    """

    path = Path(__file__).resolve().parents[1] / "pyproject.toml"
    pyproject = toml.loads(open(str(path)).read())
    pyproject_version = pyproject["tool"]["poetry"]["version"]

    package_init_version = table2sql.__version__

    assert package_init_version == pyproject_version
