from pathlib import Path
from typing import Annotated

import typer
from rich import print

from navfitx.models import Fitrep

app = typer.Typer(add_completion=False, no_args_is_help=True)


@app.callback()
def callback():
    """
    Toml tools for NAVFITX.
    """
    pass


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
            help="The path to the input TOML file.",
            exists=True,
            dir_okay=False,
            readable=True,
        ),
    ],
    output: Annotated[
        str,
        typer.Option(
            "--output",
            "-o",
            help="The name or path for the output PDF file.",
            writable=True,
            dir_okay=False,
        ),
    ] = "navfitx_report.pdf",
):
    """
    Generate a Performance Evaluation PDF from a .toml file.
    """
    pass


@app.command()
def template(
    type_of_report: Annotated[
        str,
        typer.Option(
            "--type",
            "-t",
            help="The template type, either 'eval', 'chiefeval', or 'fitrep'.",
            case_sensitive=False,
        ),
    ],
    outfile: Annotated[
        Path,
        typer.Option(
            "--output",
            "-o",
            help="The name or path for the output JSON file.",
            writable=True,
            dir_okay=False,
        ),
    ],
):
    """
    Create a NAVFITX compatible .toml template file. This file can be imported in NAVFITX later,
    or directly converted to PDF using the NAVFITX CLI.
    """
    match type_of_report.lower():
        case "eval" | "chiefeval":
            print("Not yet implemented.")
        case "fitrep":
            fitrep = Fitrep()
            print(fitrep.model_json_schema())
            with outfile.open("w") as f:
                for field in fitrep.model_dump(exclude={"id"}):
                    f.write(f"[{field}]\n\n")
        case _:
            raise typer.BadParameter("Invalid type of report. Must be one of: eval, chiefeval, fitrep")
