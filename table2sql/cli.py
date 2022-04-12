import logging
from typing import Optional

import click

from .main import convert_csv_to_insert_statement

logger = logging.getLogger()


@click.command()
@click.argument(
    "filename",
    type=str,
)
@click.option(
    "--output-table",
    required=True,
    type=str,
    help="Name of table to use in SQL insert statement",
)
@click.option("--delimiter", default=",", type=str, help="Delimiter of CSV file", show_default=True)
@click.option(
    "--has-types-row",
    is_flag=True,
    help="If file contains row with types as row 1",
)
@click.option("--output-file", default=None, help="Name of file to write SQL insert to")
def cli(
    filename: str,
    output_table: str,
    delimiter: Optional[str],
    has_types_row: Optional[bool],
    output_file: Optional[str],
):
    """Converts given table file to SQL insert statements."""
    file_extension = filename.split(".")[-1]
    if file_extension == "csv":
        insert_statement = convert_csv_to_insert_statement(
            filename, output_table=output_table, delimiter=delimiter, types_row=has_types_row
        )
    else:
        raise NotImplementedError(f"'{file_extension}' is not supported")

    print(insert_statement)
    if output_file:
        with open(output_file, "w") as f:
            print(f"\nOutput written to {output_file}")
            f.write(insert_statement)


if __name__ == "__main__":
    cli()
