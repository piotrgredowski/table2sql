from typing import Any, List, Optional, Tuple, cast

from openpyxl import load_workbook
from openpyxl.worksheet.worksheet import Worksheet


def get_list_of_tuples_from_excel(
    path_to_file: str, sheet_name: Optional[str] = None
) -> List[Tuple[Any, ...]]:
    workbook = load_workbook(filename=path_to_file)
    if sheet_name:
        sheet = cast(Worksheet, workbook[sheet_name])
    else:
        sheet = workbook.active

    return list(sheet.values)
