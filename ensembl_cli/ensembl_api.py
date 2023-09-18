import requests
from typing import List, Dict

DEFAULT_SPECIES = "human"
SERVER = "https://rest.ensembl.org"
HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}


def post_ensembl(endpoint: str, params: Dict) -> Dict:
    try:
        response = requests.post(SERVER + endpoint, headers=HEADERS, json=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as error:
        raise error


def get_ensembl(endpoint: str) -> Dict:
    try:
        r = requests.get(SERVER + endpoint, headers=HEADERS)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as error:
        raise error


def get_consequences_by_variant_ids(ids: List[str]) -> List[Dict]:
    return post_ensembl(f"/vep/{DEFAULT_SPECIES}/id", {"ids": ids})


def get_consequences_by_variant_id(id: str) -> List[Dict]:
    return get_ensembl(f"/vep/{DEFAULT_SPECIES}/id/{id}")
