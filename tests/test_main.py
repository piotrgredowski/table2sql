import os

import pytest

from table2sql.main import convert_table_file_to_insert_statement
from tests import TEST_TABLE_NAME
from tests.helpers import save_to_csv, save_to_excel


def test_not_supported_file_extension_raises_error():
    with pytest.raises(NotImplementedError) as excinfo:
        convert_table_file_to_insert_statement(
            path_to_file="./test_file.xls",
            output_table="not relevant",
            delimiter="not relevant",
            has_types_row=False,
        )
        assert "'xls' file extensions is not supported" in str(excinfo.value)


test_config_with_csvs = [
    {
        "input_data": """
a,b,c,d
1,2,3,4
5,6,7,8
""",
        "delimiter": ",",
        "has_types_row": False,
        "table_name": TEST_TABLE_NAME,
        "expected": """
INSERT INTO test.table (a, b, c, d)
VALUES (1, 2, 3, 4), (5, 6, 7, 8);""",
    },
    {
        "input_data": """
a;b;c;d
1;2;3;4
5;6;7;8
""",
        "delimiter": ";",
        "has_types_row": False,
        "table_name": TEST_TABLE_NAME,
        "expected": """
INSERT INTO test.table (a, b, c, d)
VALUES (1, 2, 3, 4), (5, 6, 7, 8);
""",
    },
    {
        "input_data": """
a;b;c;d
int;str;float;int
1;2;3;4
5;6;7;8
""",
        "delimiter": ";",
        "has_types_row": True,
        "table_name": TEST_TABLE_NAME,
        "expected": """
INSERT INTO test.table (a, b, c, d)
VALUES (1, '2', 3.0, 4), (5, '6', 7.0, 8);
""",
    },
    {
        "input_data": """
a;b;c;d
int;str;float;sql
1;2;3;(SELECT 1)
5;6;7;(SELECT 1)
""",
        "delimiter": ";",
        "has_types_row": True,
        "table_name": TEST_TABLE_NAME,
        "expected": """
INSERT INTO test.table (a, b, c, d)
VALUES (1, '2', 3.0, (SELECT 1)), (5, '6', 7.0, (SELECT 1));
""",
    },
    {
        "input_data": """
a;b;c;d
int;str;float;sql
1;2;3;(SELECT id FROM another.table WHERE name = 'Paul')
5;6;7;(SELECT id FROM another.table WHERE name = 'Paul')
""",
        "delimiter": ";",
        "has_types_row": True,
        "table_name": TEST_TABLE_NAME,
        "expected": """
INSERT INTO test.table (a, b, c, d)
VALUES (1, '2', 3.0, (SELECT id FROM another.table WHERE name = 'Paul')), (5, '6', 7.0, (SELECT id FROM another.table WHERE name = 'Paul'));
""",
    },
    {
        "input_data": """
a;b
not_implemented_type;str
1;2
5;6
""",
        "delimiter": ";",
        "has_types_row": True,
        "table_name": TEST_TABLE_NAME,
        "expected": """
INSERT INTO test.table (a, b)
VALUES (1, '2'), (5, '6');
""",
    },
]

test_config_with_csvs_as_tuples = [c.values() for c in test_config_with_csvs]


@pytest.mark.parametrize(
    "test_data, delimiter, has_types_row, table_name, expected", test_config_with_csvs_as_tuples
)
def test_convert_table_file_to_insert_statement_from_csv(
    test_data, delimiter, has_types_row, table_name, expected
):
    expected = expected.strip()
    test_data = test_data.strip()

    test_filename = save_to_csv(test_data)

    result_insert_statement = convert_table_file_to_insert_statement(
        path_to_file=test_filename,
        delimiter=delimiter,
        output_table=table_name,
        has_types_row=has_types_row,
    )

    os.remove(test_filename)

    assert result_insert_statement == expected


test_config_with_excels = [
    {
        "input_data": [
            ("a", "b", "c", "d"),
            ("int", "str", "float", "sql"),
            (1, 2, 3, "(SELECT 1)"),
            (5, 6, 7, "(SELECT 1)"),
        ],
        "has_types_row": True,
        "table_name": TEST_TABLE_NAME,
        "expected": """
INSERT INTO test.table (a, b, c, d)
VALUES (1, '2', 3.0, (SELECT 1)), (5, '6', 7.0, (SELECT 1));""",
    },
]
test_config_with_excels_as_tuples = [c.values() for c in test_config_with_excels]


@pytest.mark.parametrize(
    "test_data, has_types_row, table_name, expected", test_config_with_excels_as_tuples
)
def test_convert_table_file_to_insert_statement_from_excel(
    test_data, has_types_row, table_name, expected
):
    expected = expected.strip()

    test_filename = save_to_excel(test_data)

    result_insert_statement = convert_table_file_to_insert_statement(
        path_to_file=test_filename,
        output_table=table_name,
        has_types_row=has_types_row,
    )

    os.remove(test_filename)

    assert result_insert_statement == expected


def test_convert_table_file_to_insert_statement_from_excel_with_multiple_sheets():
    test_data = [
        ("a", "b", "c", "d"),
        ("int", "str", "float", "sql"),
        (1, 2, 3, "(SELECT 1)"),
        (5, 6, 7, "(SELECT 1)"),
    ]

    sheet_name = "test sheet"

    expected = """
INSERT INTO test.table (a, b, c, d)
VALUES (1, '2', 3.0, (SELECT 1)), (5, '6', 7.0, (SELECT 1));""".strip()

    test_filename = save_to_excel(
        test_data, sheet_name=sheet_name, additional_sheets=["1", "2", "3"]
    )

    result_insert_statement = convert_table_file_to_insert_statement(
        path_to_file=test_filename,
        output_table=TEST_TABLE_NAME,
        has_types_row=True,
        sheet_name=sheet_name,
    )

    os.remove(test_filename)

    assert result_insert_statement == expected
