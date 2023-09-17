import requests
from typing import List, Dict

DEFAULT_SPECIES = "human"
SERVER = "https://rest.ensembl.org"
HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}


def post_ensembl(extension: str, params: Dict) -> Dict:
    r = requests.post(SERVER + extension, headers=HEADERS, json=params)
    r.raise_for_status()
    return r.json()


def get_ensembl(extension: str) -> Dict:
    r = requests.get(SERVER + extension, headers=HEADERS)
    r.raise_for_status()
    return r.json()


def get_consequences_by_variant_ids(ids: List[str]) -> List[Dict]:
    return post_ensembl(f"/vep/{DEFAULT_SPECIES}/id", {"ids": ids})
