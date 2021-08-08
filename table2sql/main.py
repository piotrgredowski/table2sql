import csv
import logging
from typing import Callable, List, Optional

logger = logging.getLogger()

INSERT_TEMPLATE = """
INSERT INTO {table_name} {column_names}
VALUES {values};
""".strip()

TYPES_MAP = {
    "int": int,
    "float": float,
    "str": lambda value: f"'{value}'",
    "sql": lambda sql: sql,
}


def _get_columns_formatted(column_names: List[str]):
    return f"({', '.join(column_names)})"


def _get_values_formatted(values: List[str], types: Optional[List[Callable]]):
    values_ = []
    for row in values:
        if types:
            row = [str(type_(value)) for type_, value in zip(types, row)]

        values_.append(f'({", ".join(row)})')

    return ", ".join(values_)


def _get_insert_statement_formatted(
    table_name: str, column_names_formatted: str, values_formatted: str
):
    return INSERT_TEMPLATE.format(
        table_name=table_name, column_names=column_names_formatted, values=values_formatted
    )


def _get_types_functions(types_str: list[str]):
    types_functions = []
    for type_str in types_str:
        try:

            type_ = TYPES_MAP[type_str]
        except KeyError:
            type_ = str
            logger.warning(
                f"{type_str} was not found in types map. "
                f"Available types: {', '.join(TYPES_MAP.keys())}"
            )
        types_functions.append(type_)
    return types_functions


def convert_csv_to_insert_statement(
    filename: str, output_table: str, delimiter=",", types_row=False
):
    """Converts CSV file to SQL insert statements.

    If file doesn't contain row with types as second row - every value is treated as string and
    will be available in insert statement with single quotes.

    If file contain row with types and `types_row` argument is set to `True` - types will be used
    to convert columns to given types.

    Args:
        filename (str): Name of CSV file containing data to be converted to SQL insert statements.
        output_table (str): Name of table into which data should be inserted.
        delimiter (str, optional): Delimiter of given CSV file. Defaults to ",".
        types_row (bool, optional): If second row of CSV file contains row with types
          (from `TYPES_MAP`). Defaults to False.

    Returns:
        str: SQL insert statement
    """
    input_file_ = open(filename)
    input_file = csv.reader(input_file_, delimiter=delimiter)

    types = None
    if types_row:
        [column_names, types_str, *values] = input_file
        types = _get_types_functions(types_str)
    else:
        [column_names, *values] = input_file

    column_names_formatted = _get_columns_formatted(column_names)
    values_formatted = _get_values_formatted(values, types=types)

    return _get_insert_statement_formatted(
        table_name=output_table,
        column_names_formatted=column_names_formatted,
        values_formatted=values_formatted,
    )
