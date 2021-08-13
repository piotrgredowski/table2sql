import os

import pytest

from table2sql.main import convert_table_file_to_insert_statement
from tests import TEST_TABLE_NAME
from tests.helpers import save_to_file

test_config = [
    {
        "input_data": """
a,b,c,d
1,2,3,4
5,6,7,8
""",
        "delimiter": ",",
        "types_row": False,
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
        "types_row": False,
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
        "types_row": True,
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
        "types_row": True,
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
        "types_row": True,
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
        "types_row": True,
        "table_name": TEST_TABLE_NAME,
        "expected": """
INSERT INTO test.table (a, b)
VALUES (1, '2'), (5, '6');
""",
    },
]

test_config_as_tuples = [c.values() for c in test_config]


@pytest.mark.parametrize(
    "test_data, delimiter, types_row, table_name, expected", test_config_as_tuples
)
def test_convert_csv_to_insert_statement_from_csv(
    test_data, delimiter, types_row, table_name, expected
):
    expected = expected.strip()
    test_data = test_data.strip()

    test_csv_filename = save_to_file(test_data)

    result_insert_statement = convert_table_file_to_insert_statement(
        filename=test_csv_filename,
        delimiter=delimiter,
        output_table=table_name,
        types_row=types_row,
    )

    os.remove(test_csv_filename)

    assert result_insert_statement == expected
