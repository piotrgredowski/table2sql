import logging
from typing import Optional

import click

from .main import TYPES_MAP, convert_table_file_to_insert_statement

logger = logging.getLogger()


@click.command()
@click.argument(
    "path-to-file",
    type=str,
)
@click.option(
    "--output-table",
    required=True,
    type=str,
    help="Name of table to use in SQL insert statement.",
)
@click.option(
    "--delimiter", default=",", type=str, help="Delimiter of CSV file.", show_default=True
)
@click.option(
    "--has-types-row",
    is_flag=True,
    help=(
        "If file contains row with types as row 1 (second row in file). "
        f"Available types: {', '.join(TYPES_MAP.keys())}."
    ),
)
@click.option("--output-file", default=None, help="Name of file to write SQL insert to.")
def table2sql(
    path_to_file: str,
    output_table: str,
    delimiter: Optional[str],
    has_types_row: Optional[bool],
    output_file: Optional[str],
):
    """Converts given table file to SQL insert statements and prints it."""

    insert_statement = convert_table_file_to_insert_statement(
        path_to_file=path_to_file,
        output_table=output_table,
        delimiter=delimiter,
        has_types_row=has_types_row,
    )

    print(insert_statement)
    if output_file:
        with open(output_file, "w") as f:
            print(f"\nOutput written to {output_file}")
            f.write(insert_statement)
