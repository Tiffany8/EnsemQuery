import os
import pytest
from pathlib import Path


@pytest.mark.e2e
def test_valid_rsid_variant_ids(cli_runner, valid_rsid_variant_ids):
    results = cli_runner(
        [
            "vep",
            "ids",
            valid_rsid_variant_ids["input_file_path"],
            "--output-fn",
            valid_rsid_variant_ids["output_fn"],
            "--output-dir",
            valid_rsid_variant_ids["output_dir"],
        ]
    )

    output_file_path = os.path.join(
        valid_rsid_variant_ids["output_dir"], valid_rsid_variant_ids["output_fn"]
    )

    assert results.exit_code == 0
    assert output_file_path in results.stdout

    with open(output_file_path, "r") as f:
        lines = f.readlines()
        assert len(lines) == 3


@pytest.mark.e2e
def test_some_fake_rsid_variant_ids(cli_runner, some_fake_rsid_variant_ids):
    data = some_fake_rsid_variant_ids
    results = cli_runner(
        [
            "vep",
            "ids",
            data["input_file_path"],
            "--output-fn",
            data["output_fn"],
            "--output-dir",
            data["output_dir"],
        ]
    )

    output_file_path = os.path.join(data["output_dir"], data["output_fn"])

    assert results.exit_code == 0
    assert output_file_path in results.stdout

    with open(output_file_path, "r") as f:
        lines = f.readlines()
        assert len(lines) == 2


@pytest.mark.e2e
def test_no_valid_rsid_variant_ids(cli_runner, no_valid_rsid_variant_ids):
    data = no_valid_rsid_variant_ids
    results = cli_runner(
        [
            "vep",
            "ids",
            data["input_file_path"],
            "--output-fn",
            data["output_fn"],
            "--output-dir",
            data["output_dir"],
        ]
    )

    output_file_path = os.path.join(data["output_dir"], data["output_fn"])

    assert results.exit_code == 0
    assert "No ids successfully fetched" in results.stdout
    assert not Path(output_file_path).exists()


@pytest.mark.e2e
def test_cosmic_variant_ids(cli_runner, cosmic_variant_id):
    data = cosmic_variant_id
    results = cli_runner(
        [
            "vep",
            "ids",
            data["input_file_path"],
            "--output-fn",
            data["output_fn"],
            "--output-dir",
            data["output_dir"],
        ]
    )

    output_file_path = os.path.join(data["output_dir"], data["output_fn"])

    assert results.exit_code == 0
    assert output_file_path in results.stdout

    with open(output_file_path, "r") as f:
        lines = f.readlines()
        assert len(lines) == 2


@pytest.mark.e2e
def test_empty_input_file(cli_runner, empty_input_file):
    data = empty_input_file
    results = cli_runner(
        [
            "vep",
            "ids",
            data["input_file_path"],
            "--output-fn",
            data["output_fn"],
            "--output-dir",
            data["output_dir"],
        ]
    )

    assert results.exit_code == 0
    assert "File is empty" in results.stdout
