import csv
from datetime import datetime as dt
from enum import Enum
import os
from pathlib import Path
from typing import Dict, List, Generator

from ensembl_cli.utils import is_valid_variant_id


CHUNK_SIZE = 1024


class FileFormatInfo(Enum):
    TAB = ("\t", ".tsv")
    CSV = (",", ".csv")

    def __init__(self, delimiter, extension):
        self.delimiter = delimiter
        self.extension = extension


class FileReader:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def read_ids_from_file(self):
        for chunk in self.read_file():
            ids = FileReader.filter_valid_ids(chunk)
            yield ids

    def read_file(self) -> Generator[List[str], None, None]:
        if not os.path.exists(self.file_path):
            print("Error: File does not exist")
        with open(self.file_path, "r") as f:
            while True:
                chunk = f.readlines(CHUNK_SIZE)

                if not chunk:
                    break

                print("Processing chunk")
                chunk = [line.rstrip() for line in chunk]
                yield chunk

    @staticmethod
    def filter_valid_ids(chunk: List[str]) -> bool:
        return [line for line in chunk if is_valid_variant_id(line)]


class FileWriter:
    def __init__(
        self, file_name: str = None, format: FileFormatInfo = FileFormatInfo.TAB
    ):
        self.format = format
        self.filename = file_name if file_name else self.generate_file_name()
        self.file_path = Path(
            os.getcwd(), Path(self.filename).with_suffix(self.format.extension)
        )

    def generate_file_name(self):
        return f"output_{dt.now().strftime('%Y%m%d_%H%M%S')}"

    def write_file(self, rows: List[Dict]):
        file_exists = self.file_path.exists()
        with open(self.file_path, "a", newline="") as file:
            writer = csv.DictWriter(
                file, fieldnames=rows[0].keys(), delimiter=self.format.delimiter
            )

            if not file_exists:
                writer.writeheader()

            writer.writerows(rows)
