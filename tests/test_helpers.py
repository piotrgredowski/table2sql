import pytest

from table2sql.helpers import get_sibling_file_path

test_config = [
    {"base_file": "/a/b/c/d.py", "target_file": "e.html", "expected": "/a/b/c/e.html"},
    {"base_file": "d.py", "target_file": "e.html", "expected": "e.html"},
    {"base_file": "/a/b/d.py", "target_file": "../../e.html", "expected": "/a/b/../../e.html"},
]

test_config_as_tuple = [c.values() for c in test_config]


@pytest.mark.parametrize("base_file, target_file, expected", test_config_as_tuple)
def test_get_sibling_path(base_file, target_file, expected):
    result = get_sibling_file_path(base_file=base_file, target_file_name=target_file)

    assert result == expected
