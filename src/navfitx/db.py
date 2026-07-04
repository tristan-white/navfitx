"""
Functinos for interacting with the NAVFITX database.
"""

# import pyodbc
# from pydantic import BaseModel, Field
from pathlib import Path

from sqlmodel import Session, create_engine

from .models import Report


def add_report_to_db(db_path: Path, report: Report):
    # TODO: confirm that db_path is to a sqlite database with appropriate schema
    engine = create_engine(f"sqlite:///{db_path}")
    with Session(engine) as session:
        session.add(report)
        session.commit()


def add_fitrep_to_db(db_path: Path, report: Report):
    engine = create_engine(f"sqlite:///{db_path}")
    with Session(engine) as session:
        session.add(report)
        session.commit()


# def get_enlisted_summary_group_avg(db_path: Path, rate: str, desig: str, rs: str, period_end: date, uic) -> float:
#     """
#     Get the average summary group for enlisted sailors in a given reporting senior's command.
#     """
#     engine = create_engine(f"sqlite:///{db_path}")
#     with Session(engine) as session:
#         avg_summary_group = (
#             session.query(Report)
#             .filter(
#                 Report.reporting_senior == rs,
#                 Report.period_end == period_end,
#                 Report.uic == uic,
#                 Report.rate.in_(["E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8", "E9"]),
#             )
#             .with_entities(func.avg(Report.summary_group))
#             .scalar()
#         )
#         return avg_summary_group


"""
def get_reports_from_accdb(db: Path) -> list[Report]:
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
            nob=row.NOB,
            regular=row.Regular,
            concurrent=row.Concurrent,
            ops_cdr=row.OpsCdr,
            physical_readiness=row.PhysicalReadiness,
            billet_subcat=row.BilletSubcat,
            reporting_senior=row.ReportingSenior,
            rs_grade=row.RSGrade,
            rs_desig=row.RSDesig,
            rs_title=row.RSTitle,
            rs_uic=row.RSUIC,
            rs_ssn=row.RSSSN,
            achievements=row.Achievements,
            primary_duty=row.PrimaryDuty,
            duties=row.Duties,
            date_counseled=row.DateCounseled,
            counselor=row.Counselor,
            prof=row.PROF,
            qual=row.QUAL,
            eo=row.EO,
            mil=row.MIL,
            pa=row.PA,
            team=row.TEAM,
            mis=row.MIS,
            tac=row.TAC,
            recommend_1=row.RecommendA,
            recommend_2=row.RecommendB,
            rater=row.Rater,
            rater_date=row.RaterDate,
            comments_pitch=row.CommentsPitch,
            comments=row.Comments,
            qualifications=row.Qualifications,
            promotion_recom=row.PromotionRecom,
            summary_sp=row.SummarySP,
            summary_prog=row.SummaryProg,
            summary_mp=row.SummaryMP,
            summary_ep=row.SummaryEP,
            retention_yes=row.RetentionYes,
            retention_no=row.RetentionNo,
            rs_address=row.RSAddress,
            senior_rater=row.SeniorRater,
            senior_rater_date=row.SeniorRaterDate,
            statement_yes=row.StatementYes,
            statement_no=row.StatementNo,
            rs_info=row.RSInfo,
            user_comments=row.UserComments,
        )
        reports.append(report)
    cnxn.close()
    return reports


def convert_accdb_to_sqlite(accdb: Path, sqlite: Path):
    reports = get_reports_from_accdb(accdb)
    engine = create_engine(f"sqlite:///{sqlite}")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        for report in reports:
            session.add(report)
        session.commit()

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
    reports = get_reports_from_accdb(file)
    for report in reports:
        print(report)

@app.command(no_args_is_help=True)
def convert_accdb(
    accdb: Annotated[
        Path,
        typer.Option(
            "-a",
            "--accdb",
            help="Path to the Microsoft Access Database file (.accdb)",
            exists=True,
            dir_okay=False,
        ),
    ],
    output: Annotated[
        Path,
        typer.Option(
            "-o",
            "--output",
            help="Path to the Microsoft Access Database file (.accdb)",
            dir_okay=False,
        ),
    ],
):
    '''
    Convert a Microsoft Access Database file (.accdb) from NAVFIT98 to a sqlite database for NAVFITX.
    '''
    assert not output.exists()
    convert_accdb_to_sqlite(accdb, output)
    print(f"[green]Converted database written to {output}")
"""
