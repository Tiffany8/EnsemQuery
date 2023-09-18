from ensembl_cli import ensembl_api as api
from ensembl_cli.handlers.file_handler import FileReader, FileWriter
from ensembl_cli.handlers.file_spec import FileSpec


class VEPService:
    """
    Fetch variant consequences from Ensembl REST API
    """

    def __init__(
        self,
        output_file_writer: FileWriter,
        file_spec: FileSpec,
        input_file_reader: FileReader,
    ):
        self.input_reader = input_file_reader
        self.output_writer = output_file_writer
        self.file_spec = file_spec
        self.error_message = None

    def fetch_and_process_by_variant_identifiers(self):
        try:
            # Read IDs from file
            for ids in self.input_reader.read_ids_from_file():
                # Fetch data from Ensembl
                raw_data = api.get_consequences_by_variant_ids(ids)

                # Parse the data based on FileSpec rules
                parsed_data = self.file_spec.parse_data(raw_data)

                # Write the parsed data to a new file
                self.output_writer.write_file(parsed_data)
        except Exception as error:
            self.error_message = str(error)

    def fetch_and_by_hgvs_notations(self, hgvs_annotations):
        pass
