import time
import requests
from typing import List, Dict

DEFAULT_SPECIES = "human"
SERVER = "https://rest.ensembl.org"
HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}


#
class EnsemblRestClient:
    """
    A client for interacting with the Ensembl REST API.

    This was taken from Ensembl REST API documentation,
    updated with the requests library (as opposed to urllib),
    then modified slightly to handle errors for the cli needs.

    See https://github.com/Ensembl/ensembl-rest/wiki/Example-Python-Client

    Attributes:
        server (str): The base URL of the Ensembl REST API.
        reqs_per_sec (int): The maximum number of requests per second to make to the API
        req_count (int): The current count of requests made.
        last_req (float): The timestamp of the last request made.
    """

    def __init__(self, server=SERVER, reqs_per_sec=15):
        self.server = server
        self.reqs_per_sec = reqs_per_sec
        self.req_count = 0
        self.last_req = 0

    def _perform_request(self, method, url, headers=HEADERS, params=None, data=None):
        try:
            response = requests.request(
                method, url, headers=headers, params=params, json=data
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as error:
            if error.response.status_code == 429:
                retry = error.response.headers.get("Retry-After", 1)
                time.sleep(float(retry))
                return self._perform_request(method, url, headers, data)
            else:
                # Trying to return a more useful error message for the end user
                # for example, rather than "400 Client Error: Bad Request for url:
                # https://rest.ensembl.org/vep/human/id",
                # the user will see "No variant found with ID 'rs1'"
                raise Exception(response.json().get("error")) or error

    def get(self, endpoint, params=None):
        return self._perform_request("GET", self.server + endpoint, params=params)

    def post(self, endpoint, data=None):
        return self._perform_request("POST", self.server + endpoint, data=data)


def get_consequences_by_variant_ids(ids: List[str]) -> List[Dict]:
    """Batch fetch variant consequences for multiple variant ids."""
    ensembl_client = EnsemblRestClient()
    return ensembl_client.post(f"/vep/{DEFAULT_SPECIES}/id", {"ids": ids})


def get_consequences_by_variant_id(id: str) -> List[Dict]:
    """Fetch variant consequences for a single variant id."""
    ensembl_client = EnsemblRestClient()
    return ensembl_client.get(f"/vep/{DEFAULT_SPECIES}/id/{id}")
