import re

from rich.console import Console
from rich.table import Table
from rich import box


def is_valid_variant_id(id: str) -> bool:
    dbsnp_pattern = "^rs\d+$"
    cosmic_pattern = "^COSM\d+$"
    hgmd_pattern = "^HGMD:\d+$"

    return (
        re.match(dbsnp_pattern, id)
        or re.match(cosmic_pattern, id)
        or re.match(hgmd_pattern, id)
    )


def print_table_with_message(message: str, style: str = None):
    console = Console()
    table = Table(box=box.ROUNDED)
    table.show_header = False
    if style:
        table.style = style
    table.add_row(message)
    console.print(table)
