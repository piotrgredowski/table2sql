import pytest

from table2sql.converters.from_excel import get_list_of_tuples_from_excel
from table2sql.helpers import get_sibling_file_path


def test_not_supported_file_extension_raises_error():
    with pytest.raises(NotImplementedError) as excinfo:
        get_list_of_tuples_from_excel(path_to_file="./test_file.xls")
        assert "'xls' file extensions is not supported" in str(excinfo.value)


def test_getting_list_of_tuples_from_excel():
    expected = [
        ("a", "b", "c", "d"),
        ("int", "str", "float", "sql"),
        (1, 2, 3, "(SELECT 1)"),
        (5, 6, 7, "(SELECT 1)"),
    ]

    list_of_tuples = get_list_of_tuples_from_excel(
        path_to_file=get_sibling_file_path(__file__, "./test_file.xlsx")
    )
    assert list_of_tuples == expected
