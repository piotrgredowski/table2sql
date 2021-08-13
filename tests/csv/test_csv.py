from table2sql.converters.from_csv import get_list_of_tuples_from_csv
from table2sql.helpers import get_sibling_file_path


def test_get_list_of_tuples_from_csv():
    expected = [
        ("a", "b", "c", "d"),
        ("int", "str", "float", "sql"),
        ("1", "2", "3", "(SELECT 1)"),
        ("5", "6", "7", "(SELECT 1)"),
    ]

    list_of_tuples = get_list_of_tuples_from_csv(
        path_to_file=get_sibling_file_path(base_file=__file__, target_file_name="test_file.csv"),
        delimiter=";",
    )

    assert list_of_tuples == expected
