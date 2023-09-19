import pytest
from unittest.mock import Mock, patch

from ensemquery.services.vep_service import VEPService


@pytest.fixture
def vep_service():
    mock_output_writer = Mock()
    mock_file_spec = Mock()
    mock_input_reader = Mock()
    return VEPService(mock_output_writer, mock_file_spec, mock_input_reader)


def test_fetch_and_process_by_variant_identifiers_success(vep_service):
    mock_api_response = [{"id": "id1"}, {"id": "id2"}]
    vep_service.input_reader.read_ids_from_file.return_value = [["id1", "id2"]]
    vep_service.file_spec.parse_data.return_value = "parsed_data"

    with patch(
        "ensemquery.ensembl_api.get_consequences_by_variant_ids",
        return_value=mock_api_response,
    ):
        vep_service.fetch_and_process_bulk()

        vep_service.output_writer.write_file.assert_called_with("parsed_data")


def test_fetch_and_process_by_variant_identifiers_failure(vep_service):
    vep_service.input_reader.read_ids_from_file.side_effect = Exception("Read error")

    vep_service.fetch_and_process_bulk()

    assert vep_service.error_message == "Read error"
