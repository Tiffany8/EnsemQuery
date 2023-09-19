import os
from functools import partial

import pytest
from typer.testing import CliRunner

from ensembl_cli.cli import app


@pytest.fixture
def cli_runner():
    runner = CliRunner()
    return partial(runner.invoke, app)


@pytest.fixture
def data_dir():
    return os.path.join(os.path.dirname(__file__), "mock-data")


@pytest.fixture
def valid_rsid_variant_ids(data_dir):
    # Create the valid file in the data directory
    txt_data = "rs7412\nrs7903146"
    with open(os.path.join(data_dir, "valid_rsid_variant_ids.txt"), "w") as file:
        file.write(txt_data)

    yield {
        "input_file_path": os.path.join(data_dir, "valid_rsid_variant_ids.txt"),
        "output_fn": "valid_rsid_variant_ids_output.tsv",
        "output_dir": data_dir,
    }

    # Clean up the created files after the test
    os.remove(os.path.join(data_dir, "valid_rsid_variant_ids.txt"))
    os.remove(os.path.join(data_dir, "valid_rsid_variant_ids_output.tsv"))


@pytest.fixture
def some_fake_rsid_variant_ids(data_dir):
    input_file_path = os.path.join(data_dir, "some_fake_rsid_variant_ids.txt")
    output_fn = "some_fake_rsid_variant_ids_output.tsv"

    # rs1 is not an rsid
    txt_data = "rs1\nrs7903146"
    with open(input_file_path, "w") as file:
        file.write(txt_data)

    yield {
        "input_file_path": input_file_path,
        "output_fn": output_fn,
        "output_dir": data_dir,
    }

    # Clean up the created files after the test
    os.remove(input_file_path)
    os.remove(os.path.join(data_dir, output_fn))


@pytest.fixture
def no_valid_rsid_variant_ids(data_dir):
    input_file_path = os.path.join(data_dir, "no_valid_rsid_variant_ids.txt")
    output_fn = "no_valid_rsid_variant_ids_output.tsv"

    # rs1 is not an rsid
    txt_data = "rs1"
    with open(input_file_path, "w") as file:
        file.write(txt_data)

    yield {
        "input_file_path": input_file_path,
        "output_fn": output_fn,
        "output_dir": data_dir,
    }

    # Clean up the created files after the test
    os.remove(input_file_path)


@pytest.fixture
def empty_input_file(data_dir):
    input_file_path = os.path.join(data_dir, "empty_input_file.txt")
    output_fn = "empty_input_file_output.tsv"

    txt_data = ""
    with open(input_file_path, "w") as file:
        file.write(txt_data)

    yield {
        "input_file_path": input_file_path,
        "output_fn": output_fn,
        "output_dir": data_dir,
    }

    # Clean up the created files after the test
    os.remove(input_file_path)


@pytest.fixture
def invalid_file_extension(data_dir):
    input_file_path = os.path.join(data_dir, "invalid_file_extension.csv")
    output_fn = "invalid_file_extension_output.tsv"

    txt_data = "rs7903146"
    with open(input_file_path, "w") as file:
        file.write(txt_data)

    yield {
        "input_file_path": input_file_path,
        "output_fn": output_fn,
        "output_dir": data_dir,
    }

    # Clean up the created files after the test
    os.remove(input_file_path)
    os.remove(os.path.join(data_dir, output_fn))


@pytest.fixture
def invalid_file_content(data_dir):
    input_file_path = os.path.join(data_dir, "invalid_file_content.txt")
    output_fn = "invalid_file_content_output.tsv"

    txt_data = "one_column,two_column\nrs1,rs7903146\n"
    with open(input_file_path, "w") as file:
        file.write(txt_data)

    yield {
        "input_file_path": input_file_path,
        "output_fn": output_fn,
        "output_dir": data_dir,
    }

    # Clean up the created files after the test
    os.remove(input_file_path)
    os.remove(os.path.join(data_dir, output_fn))


@pytest.fixture
def cosmic_variant_id(data_dir):
    input_file_path = os.path.join(data_dir, "cosmic_variant_id.txt")
    output_fn = "cosmic_variant_id_output.tsv"

    txt_data = "COSM476"
    with open(input_file_path, "w") as file:
        file.write(txt_data)

    yield {
        "input_file_path": input_file_path,
        "output_fn": output_fn,
        "output_dir": data_dir,
    }

    # Clean up the created files after the test
    os.remove(input_file_path)
    os.remove(os.path.join(data_dir, output_fn))
