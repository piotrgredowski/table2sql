import os
import tempfile


def save_to_file(csv_str: str):
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(bytes(csv_str, encoding="utf-8"))
    new_filename = f.name + ".csv"
    os.rename(f.name, new_filename)

    return new_filename
