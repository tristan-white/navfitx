from datetime import date

import pyodbc
import typer
from sqlmodel import Field, SQLModel

# from pydantic import BaseModel, Field


class Reports(SQLModel, table=True):
    report_id: int = Field(
        primary_key=True,
    )
    parent: str
    report_type: str
    full_name: str
    first_name: str
    mi: str
    last_name: str
    suffix: str
    rate: str
    desig: str
    ssn: str
    active: bool
    tar: bool
    inactive: bool
    atadsw: bool
    uic: str
    ship_station: str
    promotion_status: str
    date_reported: date
    periodic: bool
    det_ind: bool
    frocking: bool
    special: bool
    from_date: date
    to_date: date
    nob: bool
    regular: bool
    concurrent: bool
    ops_cdr: bool
    physical_readiness: str
    physical_readiness2: str
    physical_readiness_dt: date
    billet_subcat: str
    rs_last_name: str
    rs_fi: str
    rs_mi: str
    reporting_senior: str
    rs_grade: str
    rs_desig: str
    rs_title: str
    rs_uic: str
    rs_ssn: str
    achievements: str
    primary_duty: str
    duties: str
    date_counseled: date
    counselor: str
    counselor_ln: str
    counselor_fi: str
    counselor_mi: str
    prof: int
    prof_dn1: str
    prof_dn2: str
    prof_dn3: str
    qual: int
    qual_dn1: str
    qual_dn2: str
    qual_dn3: str
    eo: int
    eo_dn1: str
    eo_dn2: str
    eo_dn3: str
    mil: int
    mil_dn1: str
    mil_dn2: str
    mil_dn3: str
    pa: int
    pa_dn1: str
    pa_dn2: str
    pa_dn3: str
    team: int
    team_dn1: str
    team_dn2: str
    team_dn3: str
    lead: int
    lead_dn1: str
    lead_dn2: str
    lead_dn3: str
    mis: int
    mis_dn1: str
    mis_dn2: str
    mis_dn3: str
    tac: int
    tac_dn1: str
    tac_dn2: str
    tac_dn3: str
    recommend_1: str
    recommend_2: str
    rater: str
    rater_date: date
    comments_pitch: str
    comments: str
    qualifications: str
    promotion_recom: int
    summary_rank: int
    summary_sp: str
    summary_prog: str
    summary_prom: str
    summary_mp: str
    summary_ep: str
    retention_yes: bool
    retention_no: bool
    rsca: int
    rs_address: str
    rs_address1: str
    rs_address2: str
    rs_city: str
    rs_state: str
    rs_zip_cd: str
    rs_phone: str
    rs_dsn: str
    senior_rater: str
    senior_rater_date: date
    statement_yes: bool
    statement_no: bool
    rs_info: str
    rrs_fi: str
    rrs_mi: str
    rrs_last_name: str
    rrs_grade: str
    rrs_command: str
    rrs_uic: str
    user_comments: str
    psswrd: str
    standards: str
    is_validated: str


def get_reports_from_access_db(db_path: str) -> list[Reports]:
    conn_str = (
        r"DRIVER={MDBTools};"
        rf"DBQ={db_path};"
    )
    cnxn = pyodbc.connect(conn_str)
    crsr = cnxn.cursor()
    reports = []
    # iterate through each row in the Reports table
    for row in crsr.execute("SELECT * FROM Reports"):
        report = Reports(
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


@app.command()
def test():
    """test"""
    reports = get_reports_from_access_db("./export_folder.accdb")
    for report in reports:
        print(report)


if __name__ == "__main__":
    app()
