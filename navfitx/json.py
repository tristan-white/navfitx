import json
from pathlib import Path
from typing import Annotated

import typer
from pydantic import ValidationError
from rich import print, print_json

from navfitx.models import Fitrep
from navfitx.overlay import create_fitrep_pdf

app = typer.Typer(add_completion=False, no_args_is_help=True)


@app.callback()
def callback():
    """
    JSON tools for NAVFITX.
    """
    pass


def validate_type_of_report(value: str) -> str:
    valid_types = {"eval", "chiefeval", "fitrep"}
    if value.lower() not in valid_types:
        raise typer.BadParameter(f"Invalid type of report. Must be one of: {', '.join(valid_types)}")
    return value.lower()


@app.command()
def dummy():
    fitrep = Fitrep()
    print(fitrep.model_dump_json(indent=2))


@app.command()
def pdf(
    input: Annotated[
        str,
        typer.Option(
            "--input",
            "-i",
            help="The path to the input JSON file.",
            exists=True,
            dir_okay=False,
            readable=True,
        ),
    ],
    outfile: Annotated[
        Path,
        typer.Option(
            "--outfile",
            "-o",
            help="The name or path for the output PDF file.",
            writable=True,
            dir_okay=False,
        ),
    ] = Path("navfitx_report.pdf"),
    validate: Annotated[
        bool,
        typer.Option(
            help="Whether to validate the input JSON file against the Fitrep model before generating the PDF. This must be off in order to generate incomplete reports."
        ),
    ] = True,
):
    """
    Generate a Performance Evaluation PDF from a .json file.
    """
    try:
        data = json.loads(Path(input).read_text())
    except json.JSONDecodeError as e:
        print("[red]Failed to parse JSON file. See error details below:[/red]")
        print(e)
        raise typer.Exit(code=1)

    if validate:
        try:
            fitrep = Fitrep.model_validate(data)
        except ValidationError as e:
            print("[red]Input JSON file is invalid against the Fitrep model. See error details below:[/red]")
            print(e)
            raise typer.Exit(code=1)
    else:
        fitrep = Fitrep(**data)

    create_fitrep_pdf(fitrep, outfile)


@app.command()
def template(
    type_of_report: Annotated[
        str,
        typer.Option(
            "--type-of-report",
            "-t",
            help="The template type, either 'eval', 'chiefeval', or 'fitrep'.",
            case_sensitive=False,
            callback=validate_type_of_report,
        ),
    ],
    output: Annotated[
        Path | None,
        typer.Option(
            "--output",
            "-o",
            help="The name or path for the output JSON file. If none given, template is output to stdout.",
            writable=True,
            dir_okay=False,
        ),
    ] = None,
):
    """
    Create a template .json file for users to fill out.
    """
    match type_of_report.lower():
        case "eval" | "chiefeval":
            print("Not implemented yet.")
        case "fitrep":
            fitrep = Fitrep()
            text = fitrep.model_dump_json()
            if output is not None:
                output.write_text(text)
            else:
                print_json(text)
