import pytest

from table2sql.converters.from_excel import get_list_of_tuples_from_excel
from table2sql.helpers import get_sibling_file_path


@pytest.mark.parametrize(
    "filename",
    ["test_file.xlsm", "test_file.xlsx"],
)
def test_getting_list_of_tuples_from_excel(filename):
    expected = [
        ("a", "b", "c", "d"),
        ("int", "str", "float", "sql"),
        (1, 2, 3, "(SELECT 1)"),
        (5, 6, 7, "(SELECT 1)"),
    ]

    list_of_tuples = get_list_of_tuples_from_excel(
        path_to_file=get_sibling_file_path(__file__, filename)
    )
    assert list_of_tuples == expected
