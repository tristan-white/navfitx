import webbrowser
from pathlib import Path

import pymupdf
import typer
from typing_extensions import Annotated

app = typer.Typer(no_args_is_help=True, add_completion=False)


@app.command()
def overlay(
    file: Annotated[Path, typer.Option(help="Path to the input file")],
):
    doc = pymupdf.open(file)
    page = doc[0]
    text = "Doe, John"
    position = pymupdf.Point(20, 137)  # 1 inch from top-left corner
    page.insert_text(position, text, fontsize=12, fontname="Cour")
    page.insert_text(pymupdf.Point(76, 86), "X", fontsize=12, fontname="Cour")
    doc.save("output.pdf")
    doc.close()
    webbrowser.open("output.pdf")
