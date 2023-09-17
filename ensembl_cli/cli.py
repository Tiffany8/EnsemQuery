# from enum import Enum
from pathlib import Path
from typing import Annotated

from rich import print as rprint
import typer
from ensembl_cli.handlers.file_handler import FileReader, FileWriter
from ensembl_cli.handlers.file_spec import FieldRule, FileSpec

from ensembl_cli.services.vep_service import VEPService


app = typer.Typer()
vep_app = typer.Typer(name="vep", help="Fetch variant consequences")
app.add_typer(vep_app)


@vep_app.command("ids")
def get_consequences_by_ids(
    file: Annotated[
        Path,
        typer.Argument(
            exists=True,
            file_okay=True,
            dir_okay=False,
            writable=False,
            readable=True,
            resolve_path=True,
            help="File of variant ids",
        ),
    ],
    output_fn=Annotated[str, typer.Option(help="Custom output file name")],
):
    """
    Fetch variant consequences for multiple variant ids
    (dbSNP, COSMIC and HGMD identifiers)
    """

    # Initialize VEP service with dependencies
    vep_service = VEPService(
        output_file_writer=FileWriter(file_name=output_fn),
        file_spec=FileSpec(
            [
                FieldRule("start"),
                FieldRule("end"),
                FieldRule("most_severe_consequence"),
                FieldRule(
                    field="transcript_consequences",
                    rule=lambda x: {xx.get("gene_symbol") for xx in x},
                ),
            ]
        ),
        input_file_reader=FileReader(file),
    )
    vep_service.fetch_and_process_by_variant_identifiers()

    rprint(
        ":pencil: [green] variant consequences output file:[/green] "
        f"[pink] -- {vep_service.output_writer.file_path}[/pink]"
    )


@vep_app.command("hgvs")
def get_consequences_by_hgvs_notations():
    """
    Fetch variant consequences for multiple hgvs notations
    """
    rprint(
        "[bold red]:construction: Not implemented! "
        "Coming soon! :construction:[/bold red]"
    )
