import tomllib
from pathlib import Path
from typing import Annotated

import typer
from rich import print

from navfitx.examples import build_validated_example_fitrep
from navfitx.importer import ImportSchemaError, build_fitrep_template_toml
from navfitx.models import Fitrep

app = typer.Typer(add_completion=False, no_args_is_help=True)


def validate_toml_file(file: Path) -> Path:
    """
    Validate that the provided file is a valid TOML file.
    """
    try:
        with file.open("rb") as f:
            tomllib.load(f)
    except Exception as e:
        raise typer.BadParameter(f"{e}")
    return file


@app.callback()
def callback():
    """
    Toml tools for NAVFITX.
    """
    pass


@app.command()
def example(
    output: Annotated[
        Path,
        typer.Option(
            "--output",
            "-o",
            help="The name or path for the output PDF file.",
            writable=True,
            dir_okay=False,
        ),
    ] = Path("example.toml"),
    type_of_report: Annotated[
        str,
        typer.Option(
            "--type",
            "-t",
            help="The template type, either 'eval', 'chiefeval', or 'fitrep'.",
            case_sensitive=False,
        ),
    ] = "fitrep",
):
    """
    Print an example of a valid NAVFITX .toml file to stdout.
    """
    with output.open("w", encoding="utf-8") as f:
        match type_of_report.lower():
            case "eval" | "chiefeval":
                print("Not yet implemented.")
            case "fitrep":
                f.write(build_validated_example_fitrep().model_dump_toml())
            case _:
                raise typer.BadParameter("Invalid type of report. Must be one of: eval, chiefeval, fitrep")


@app.command(no_args_is_help=True)
def pdf(
    input: Annotated[
        Path,
        typer.Option(
            "--input",
            "-i",
            help="The path to the input TOML file.",
            exists=True,
            dir_okay=False,
            readable=True,
            callback=validate_toml_file,
        ),
    ],
    output: Annotated[
        Path,
        typer.Option(
            "--output",
            "-o",
            help="The name or path for the output PDF file.",
            writable=True,
            dir_okay=False,
        ),
    ] = Path("navfitx_report.pdf"),
    validate: Annotated[
        bool,
        typer.Option(
            help="Check that the toml file contains valid and complete FITREP data before generating the PDF."
        ),
    ] = True,
):
    """
    Generate a Performance Evaluation PDF from a .toml file.
    """
    try:
        with input.open("r") as f:
            toml_str = f.read()
    except Exception as e:
        print(f"Error parsing TOML file; are you sure {input} is a valid TOML file?")
        print(f"Error details: {e}")
        raise typer.Exit(code=1)

    try:
        fitrep = Fitrep.from_toml(toml_str)
    except ImportSchemaError as e:
        print(f"Error parsing TOML file; are you sure {input} is a valid report TOML file?")
        print(f"Error details: {e}")
        raise typer.Exit(code=1)

    if validate:
        Fitrep.model_validate(fitrep)

    # TODO: ensure data is printable; ie that fields don't have text that is too long
    fitrep.create_pdf(output)
    print(f"PDF generated successfully at {output}")


@app.command(no_args_is_help=True)
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
            outfile.write_text(build_fitrep_template_toml(), encoding="utf-8")
        case _:
            raise typer.BadParameter("Invalid type of report. Must be one of: eval, chiefeval, fitrep")
