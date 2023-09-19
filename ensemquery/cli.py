# from enum import Enum
from pathlib import Path
from typing import Annotated

from rich.progress import Progress, SpinnerColumn
import typer

from ensemquery.handlers.file_handler import FileReader, FileWriter
from ensemquery.handlers.file_spec import FieldRule, FileSpec
from ensemquery.services.vep_service import VEPService
from ensemquery.utils import print_table_with_message

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
            help="Txt file of variant ids - one per line",
        ),
    ],
    output_fn=Annotated[str, typer.Option(help="Custom output file name")],
    output_dir=Annotated[str, typer.Option(help="Output file directory")],
):
    """
    Fetch variant consequences for multiple variant ids
    (dbSNP, COSMIC and HGMD identifiers)
    """

    vep_service = VEPService(
        output_file_writer=FileWriter(file_name=output_fn, file_directory=output_dir),
        file_spec=FileSpec(
            [
                FieldRule("id"),
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

    with Progress(
        SpinnerColumn(), "[progress.description]{task.description}"
    ) as progress:
        task = progress.add_task("[cyan]Fetching data...")

        vep_service.fetch_and_process_single()

        progress.remove_task(task)

    if vep_service.error_message:
        print_table_with_message(
            [
                [
                    (
                        f":warning:  [bold red]{vep_service.error_message}"
                        "[/bold red] :warning:"
                    )
                ]
            ],
            style="red",
        )
    elif not vep_service.successful_ids_count:
        print_table_with_message(
            [
                [
                    (
                        ":warning:  [bold red]No ids successfully fetched"
                        "[/bold red] :warning:"
                    )
                ]
            ],
            style="red",
        )
    else:
        rows = [
            [
                ":white_check_mark:",
                "[green]output file[/green]",
                str(vep_service.output_writer.file_path),
            ]
        ]

        if vep_service.failed_ids:
            rows.append(
                [
                    ":x:",
                    "[red]failed ids[/red]",
                    ", ".join(vep_service.failed_ids)
                    if vep_service.failed_ids
                    else "--",
                ]
            )

        print_table_with_message(rows, style="green", columns=["", "", ""])


@vep_app.command("hgvs")
def get_consequences_by_hgvs_notations():
    """
    Fetch variant consequences for multiple hgvs notations
    """
    print_table_with_message(
        [
            [
                "[orange_red1]:construction: Not implemented! "
                "Coming soon! :construction:[/orange_red1]"
            ]
        ],
        style="orange_red1",
    )
