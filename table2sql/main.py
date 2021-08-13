import logging
from typing import Callable, Iterable, List, Optional, Tuple, cast

from table2sql.converters.from_csv import get_list_of_tuples_from_csv
from table2sql.converters.from_excel import get_list_of_tuples_from_excel

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


def _get_columns_formatted(column_names: Iterable[str]):
    return f"({', '.join(column_names)})"


def _get_values_formatted(values: Iterable[str], types: Optional[List[Callable]]):
    values_ = []
    for row in values:
        if types:
            row = [str(type_(value)) for type_, value in zip(types, row)]
        else:
            row = [str(value) for value in row]
        values_.append(f'({", ".join(row)})')

    return ", ".join(values_)


def _get_insert_statement_formatted(
    table_name: str, column_names_formatted: str, values_formatted: str
):
    return INSERT_TEMPLATE.format(
        table_name=table_name, column_names=column_names_formatted, values=values_formatted
    )


def _get_types_functions(types_str: Tuple[str, ...]):
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


def _get_file_extension(file_path: str):
    return file_path.split(".")[-1]


def convert_table_file_to_insert_statement(
    path_to_file: str, output_table: str, delimiter=str, has_types_row=bool, sheet_name=None
):
    """Converts CSV file to SQL insert statements.

    If file doesn't contain row with types as second row - every value is treated as string and
    will be available in insert statement with single quotes.

    If file contain row with types and `types_row` argument is set to `True` - types will be used
    to convert columns to given types.

    Args:
        path_to_file (str): Name of file containing data to be converted to SQL insert statements.
        output_table (str): Name of table into which data should be inserted.
        delimiter (str): Delimiter of given CSV file.
        has_types_row (bool, optional): If second row of table file contains row with types
          (from `TYPES_MAP`). Defaults to False.
        sheet_name (str, optional): If file is Excel - pass sheet name which should be converted
          into insert statements.

    Returns:
        str: SQL insert statement
    """

    file_extension = _get_file_extension(path_to_file)

    if file_extension == "csv":
        rows = get_list_of_tuples_from_csv(path_to_file=path_to_file, delimiter=delimiter)
    elif file_extension in ("xlsx", "xlsm", "xltx", "xltm"):
        rows = get_list_of_tuples_from_excel(path_to_file=path_to_file, sheet_name=sheet_name)
    else:
        raise NotImplementedError(f"'.{file_extension}' file extension is not supported")

    types = None
    if has_types_row:
        [column_names, types_str, *values] = rows
        types_str = cast(Tuple[str, ...], types_str)
        types = _get_types_functions(types_str)
    else:
        [column_names, *values] = rows

    column_names_formatted = _get_columns_formatted(column_names)
    values_formatted = _get_values_formatted(values, types=types)

    return _get_insert_statement_formatted(
        table_name=output_table,
        column_names_formatted=column_names_formatted,
        values_formatted=values_formatted,
    )
