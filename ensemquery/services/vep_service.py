from ensemquery import ensembl_api as api
from ensemquery.handlers.file_handler import FileReader, FileWriter
from ensemquery.handlers.file_spec import FileSpec


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
        self.failed_ids = []
        self.successful_ids_count = 0

    def fetch_and_process_bulk(self):
        """
        Fetch variant consequences from Ensembl REST API using variant ids in bulk
        """
        try:
            # Read IDs from file
            for ids in self.input_reader.read_ids_from_file():
                # Fetch data from Ensembl
                raw_data = api.get_consequences_by_variant_ids(ids)

                # Parse the data based on FileSpec rules
                parsed_data = self.file_spec.parse_data(raw_data)

                # Update successful ids and failed ids
                self.successful_ids_count += len(raw_data)
                self.failed_ids.extend(set(ids) - set(data["id"] for data in raw_data))

                # Write the parsed data to a new file
                self.output_writer.write_file(parsed_data)
        except Exception as error:
            self.error_message = str(error)

    def fetch_and_process_single(self):
        """
        Fetch variant consequences from Ensembl REST API making single
        request per variant id.
        """
        try:
            # Read IDs from file
            for ids in self.input_reader.read_ids_from_file():
                raw_data = []

                # Fetch data from Ensembl
                for id in ids:
                    try:
                        result = api.get_consequences_by_variant_id(id)
                        if result:
                            raw_data.append(result[0])
                            self.successful_ids_count += 1
                        else:
                            self.failed_ids.append(id)
                    except Exception:
                        self.failed_ids.append(id)

                # Parse the data based on FileSpec rules
                parsed_data = self.file_spec.parse_data(raw_data)

                # Write the parsed data to a new file
                if parsed_data:
                    self.output_writer.write_file(parsed_data)
        except Exception as error:
            self.error_message = str(error)

    def fetch_and_by_hgvs_notations(self, hgvs_annotations):
        pass
