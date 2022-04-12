from typing import Any, List, Tuple

from openpyxl import load_workbook

ListOfTuples = List[Tuple[Any, ...]]


def _get_sheet_content(path_to_file: str) -> ListOfTuples:
    wb = load_workbook(filename=path_to_file)
    sheet = wb.active

    return list(sheet.values)


def get_list_of_tuples_from_excel(path_to_file: str) -> ListOfTuples:
    return _get_sheet_content(path_to_file)
