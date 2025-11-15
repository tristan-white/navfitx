from pathlib import Path

import pyodbc
import typer
from rich import print
from typing_extensions import Annotated

from .models import Report

# from pydantic import BaseModel, Field


def get_reports_from_access_db(db: Path) -> list[Report]:
    conn_str = (
        r"DRIVER={MDBTools};"
        rf"DBQ={db};"
    )
    print(conn_str)
    cnxn = pyodbc.connect(conn_str)
    crsr = cnxn.cursor()
    reports = []
    # iterate through each row in the Report table
    for row in crsr.execute("SELECT * FROM Reports"):
        report = Report(
            report_id=row.ReportID,
            parent=row.Parent,
            report_type=row.ReportType,
            full_name=row.FullName,
            first_name=row.FirstName,
            mi=row.MI,
            last_name=row.LastName,
            suffix=row.Suffix,
            rate=row.Rate,
            desig=row.Desig,
            ssn=row.SSN,
            active=row.Active,
            tar=row.TAR,
            inactive=row.Inactive,
            atadsw=row.ATADSW,
            uic=row.UIC,
            ship_station=row.ShipStation,
            promotion_status=row.PromotionStatus,
            date_reported=row.DateReported,
            periodic=row.Periodic,
            det_ind=row.DetInd,
            frocking=row.Frocking,
            special=row.Special,
            from_date=row.FromDate,
            to_date=row.ToDate,
        )
        reports.append(report)
    cnxn.close()
    return reports


app = typer.Typer(add_completion=False, no_args_is_help=True)


@app.command(no_args_is_help=True)
def print_accdb(
    file: Annotated[
        Path,
        typer.Option(
            help="Path to the Microsoft Access database file.",
            exists=True,
            dir_okay=False,
        ),
    ],
):
    reports = get_reports_from_access_db(file)
    for report in reports:
        print(report)
