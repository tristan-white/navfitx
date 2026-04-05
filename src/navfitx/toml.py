from typing import Annotated

import typer

app = typer.Typer(add_completion=False, no_args_is_help=True)


@app.callback()
def callback():
    """
    Toml tools for NAVFITX.
    """
    pass


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
):
    """
    Create a template .toml file for users to fill out.
    """
    pass
