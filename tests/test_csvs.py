import os
import tempfile

import pytest

from csv_to_sql_insert import __version__, convert_csv_to_insert_statement


def _save_to_file(csv_str):
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(bytes(csv_str, encoding="utf-8"))

    return f.name


test_config = [
    {
        "input_data": """
a,b,c,d
1,2,3,4
5,6,7,8
""",
        "delimiter": ",",
        "types_row": False,
        "table_name": "test.table",
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
        "types_row": False,
        "table_name": "test.table",
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
        "types_row": True,
        "table_name": "test.table",
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
        "types_row": True,
        "table_name": "test.table",
        "expected": """
INSERT INTO test.table (a, b, c, d)
VALUES (1, '2', 3.0, (SELECT 1)), (5, '6', 7.0, (SELECT 1));
""",
    },
]

test_config_as_tuples = [c.values() for c in test_config]


def test_version():
    assert __version__ == "0.1.0"


@pytest.mark.parametrize(
    "test_data, delimiter, types_row, table_name, expected", test_config_as_tuples
)
def test_convert_csv_to_insert_statement_from_csv(
    test_data, delimiter, types_row, table_name, expected
):
    expected = expected.strip()
    test_data = test_data.strip()

    test_csv_filename = _save_to_file(test_data)

    result_insert_statement = convert_csv_to_insert_statement(
        filename=test_csv_filename,
        delimiter=delimiter,
        output_table=table_name,
        types_row=types_row,
    )

    os.remove(test_csv_filename)

    assert result_insert_statement == expected
