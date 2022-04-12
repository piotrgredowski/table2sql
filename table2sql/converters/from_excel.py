from typing import Any, List, Tuple

from openpyxl import load_workbook

ListOfTuples = List[Tuple[Any, ...]]


def _check_file_extension(path_to_file: str):
    file_extension = path_to_file.split(".")[-1]
    if file_extension != "xlsx":
        raise NotImplementedError(f"'{file_extension}' file extensions is not supported")


def _get_sheet_content(path_to_file: str) -> ListOfTuples:
    wb = load_workbook(filename=path_to_file)
    sheet = wb.active

    return list(sheet.values)


def get_list_of_tuples_from_excel(path_to_file: str) -> ListOfTuples:
    _check_file_extension(path_to_file)
    return _get_sheet_content(path_to_file)
