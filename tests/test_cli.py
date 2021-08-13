import tempfile

import pytest
from click.testing import CliRunner

from table2sql.cli import cli
from tests import TEST_TABLE_NAME
from tests.helpers import save_to_csv

test_config = [
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
]

test_config_as_tuples = [c.values() for c in test_config]


@pytest.mark.parametrize(
    "test_data, delimiter, types_row, table_name, expected", test_config_as_tuples
)
def test_cli(test_data, delimiter, types_row, table_name, expected):

    runner = CliRunner()
    expected = expected.strip()
    test_data = test_data.strip()

    test_csv_filename = save_to_csv(test_data)

    result = runner.invoke(
        cli,
        [
            test_csv_filename,
            "--output-table",
            table_name,
            "--delimiter",
            delimiter,
            "--has-types-row",
        ],
    )
    assert result.exit_code == 0
    assert result.output.strip() == expected


@pytest.mark.parametrize(
    "test_data, delimiter, types_row, table_name, expected", test_config_as_tuples
)
def test_cli_saving_file(test_data, delimiter, types_row, table_name, expected):

    runner = CliRunner()
    expected_result = expected.strip()
    test_data = test_data.strip()

    test_csv_filename = save_to_csv(test_data)

    with tempfile.NamedTemporaryFile() as f:
        result = runner.invoke(
            cli,
            [
                test_csv_filename,
                "--output-table",
                table_name,
                "--delimiter",
                delimiter,
                "--has-types-row",
                "--output-file",
                f.name,
            ],
        )
        result_from_file = open(f.name).read()

    assert result.exit_code == 0
    assert expected_result in result.output.strip()
    assert result_from_file.strip() == expected_result


def test_cli_not_supported_file_extension():
    runner = CliRunner()

    file_extension = ".abcd"
    wrong_file = "file" + file_extension

    result = runner.invoke(
        cli,
        [
            wrong_file,
            "--output-table",
            "some.table",
        ],
    )
    assert result.exit_code == 1
    assert f"'{file_extension}' file extension is not supported"
