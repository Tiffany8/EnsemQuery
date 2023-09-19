import csv
from datetime import datetime as dt
from enum import Enum
import os
from pathlib import Path
from typing import Dict, List, Generator

from ensembl_cli.utils import is_valid_variant_id


CHUNK_SIZE = 1000


class FileFormatInfo(Enum):
    TAB = ("\t", ".tsv")
    CSV = (",", ".csv")

    def __init__(self, delimiter, extension):
        self.delimiter = delimiter
        self.extension = extension


class FileReader:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def read_ids_from_file(self) -> Generator[List[str], None, None]:
        """
        Reads IDs from a file and yields a list of valid IDs.

        Args:
            self (FileReader): The FileReader object.

        Yields:
            List[str]: A list of valid IDs extracted from the file.
        """
        for chunk in self.read_file():
            ids = FileReader.filter_valid_ids(chunk)
            yield ids

    def read_file(self) -> Generator[List[str], None, None]:
        """
        Reads the file in chunks and yields each chunk as a list of strings.

        Yields:
            List[str]: A list of strings representing a chunk of lines from the file.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file is empty.
            PermissionError: If permission is denied to read the file.
            UnicodeDecodeError: If the file cannot be decoded.
        """
        if not os.path.exists(self.file_path):
            raise FileNotFoundError("File does not exist")

        if not os.path.getsize(self.file_path):
            raise ValueError("File is empty")

        try:
            with open(self.file_path, "r") as f:
                while True:
                    chunk = f.readlines(CHUNK_SIZE)

                    if not chunk:
                        break

                    chunk = [line.rstrip() for line in chunk]
                    yield chunk

        except PermissionError:
            raise PermissionError("Permission denied to read the file")

        except UnicodeDecodeError:
            raise UnicodeDecodeError("Unable to decode the file")

    @staticmethod
    def filter_valid_ids(chunk: List[str]) -> bool:
        return [line for line in chunk if is_valid_variant_id(line)]


class FileWriter:
    def __init__(
        self,
        file_name: str = None,
        file_directory: str = None,
        format: FileFormatInfo = FileFormatInfo.TAB,
    ):
        self.format = format
        self.filename = file_name or self.generate_file_name()
        self.file_path = Path(
            file_directory or os.getcwd(),
            Path(self.filename).with_suffix(self.format.extension),
        )

    def generate_file_name(self):
        return f"output_{dt.now().strftime('%Y%m%d_%H%M%S')}"

    def write_file(self, rows: List[Dict]):
        file_exists = self.file_path.exists()
        mode = "a" if file_exists else "w"
        try:
            with open(self.file_path, mode, newline="") as file:
                writer = csv.DictWriter(
                    file, fieldnames=rows[0].keys(), delimiter=self.format.delimiter
                )

                if not file_exists:
                    writer.writeheader()

                writer.writerows(rows)
        except Exception as error:
            raise Exception(f"Error writing file: {error}")
