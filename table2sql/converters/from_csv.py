import csv
from typing import Any, List, Tuple


def get_list_of_tuples_from_csv(path_to_file: str, delimiter=",") -> List[Tuple[Any, ...]]:
    input_file_ = open(path_to_file)
    return list(tuple(row) for row in csv.reader(input_file_, delimiter=delimiter))
