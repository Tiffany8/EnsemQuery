import re


def is_valid_variant_id(id: str) -> bool:
    dbsnp_pattern = "^rs\d+$"
    cosmic_pattern = "^COSM\d+$"
    hgmd_pattern = "^HGMD:\d+$"

    return (
        re.match(dbsnp_pattern, id)
        or re.match(cosmic_pattern, id)
        or re.match(hgmd_pattern, id)
    )
