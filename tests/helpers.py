import os
import tempfile
from typing import Any, Iterable, Tuple

import openpyxl


def save_to_csv(csv_str: str):
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(bytes(csv_str, encoding="utf-8"))
    new_filename = f.name + ".csv"
    os.rename(f.name, new_filename)

    return new_filename


def save_to_excel(rows: Iterable[Tuple[Any]], file_extension: str = "xlsx"):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "range names"

    for r_idx, row in enumerate(rows, start=1):
        for c_idx, value in enumerate(row, start=1):
            _ = ws.cell(column=c_idx, row=r_idx, value=value)

    with tempfile.NamedTemporaryFile(delete=False) as f:
        new_filename = f.name + "." + file_extension
        os.rename(f.name, new_filename)
        wb.save(filename=new_filename)
    return new_filename
