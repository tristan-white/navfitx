from datetime import date

from sqlmodel import Field, SQLModel


class N98Report(SQLModel, table=True):
    """
    A SQLModel that mirrors the 'Reports' table in NAVFIT98A Access db files. This is used to convert
    NAVFIT98A Access db files (.accdb) to NAVFITX SQLite db files and vice versa.

    Args:
        report_id (int): Primary key for the report record.
        parent (str): Identifier of a parent report, if applicable.
        report_type (str): Type of report (e.g., 'FitRep').
        full_name (str): Full name of the subject.
        first_name (str): Subject's first name.
        mi (str): Subject's middle initial.
        last_name (str): Subject's last name.
        suffix (str): Name suffix (e.g., 'Jr', 'III').
        rate (str): Rate or paygrade.
        desig (str): Designator code.
        ssn (str): Social Security Number (format: XXX-XX-XXXX).
        active (bool): Active status flag.
        tar (bool): TAR status flag.
        inactive (bool): Inactive status flag.
        atadsw (bool): ATADSW flag.
        uic (str): Unit Identification Code.
        ship_station (str): Ship or station name.
        promotion_status (str): Promotion status string.
        date_reported (date): Date the report was filed.
        periodic (bool): Periodic report flag.
        det_ind (bool): Detachment individual flag.
        frocking (bool): Frocking flag.
        special (bool): Special occasion report flag.
        from_date (date): Start date of reporting period.
        to_date (date): End date of reporting period.
        nob (bool): Not observed by reporting senior flag.
        regular (bool): Regular report flag.
        concurrent (bool): Concurrent report flag.
        ops_cdr (bool): Ops commander report flag.
        physical_readiness (str): Primary physical readiness code.
        physical_readiness2 (str): Secondary physical readiness code.
        physical_readiness_dt (date): Date of physical readiness assessment.
        billet_subcat (str): Billet subcategory code.
        rs_last_name (str): Reporting senior last name.
        rs_fi (str): Reporting senior first initial.
        rs_mi (str): Reporting senior middle initial.
        reporting_senior (str): Reporting senior full name.
        rs_grade (str): Reporting senior grade.
        rs_desig (str): Reporting senior designator.
        rs_title (str): Reporting senior title.
        rs_uic (str): Reporting senior UIC.
        rs_ssn (str): Reporting senior SSN.
        achievements (str): Achievements text field.
        primary_duty (str): Primary duty description.
        duties (str): Duties text field.
        date_counseled (date): Date counseled.
        counselor (str): Counselor full name.
        counselor_ln (str): Counselor last name.
        counselor_fi (str): Counselor first initial.
        counselor_mi (str): Counselor middle initial.
        prof (int): Professional expertise score.
        prof_dn1 (str): Professional detail/notes 1.
        prof_dn2 (str): Professional detail/notes 2.
        prof_dn3 (str): Professional detail/notes 3.
        qual (int): Qualification score.
        qual_dn1 (str): Qualification detail 1.
        qual_dn2 (str): Qualification detail 2.
        qual_dn3 (str): Qualification detail 3.
        eo (int): Equal opportunity score.
        eo_dn1 (str): EO detail 1.
        eo_dn2 (str): EO detail 2.
        eo_dn3 (str): EO detail 3.
        mil (int): Military bearing score.
        mil_dn1 (str): Military detail 1.
        mil_dn2 (str): Military detail 2.
        mil_dn3 (str): Military detail 3.
        pa (int): Personnel awareness score.
        pa_dn1 (str): PA detail 1.
        pa_dn2 (str): PA detail 2.
        pa_dn3 (str): PA detail 3.
        team (int): Teamwork score.
        team_dn1 (str): Team detail 1.
        team_dn2 (str): Team detail 2.
        team_dn3 (str): Team detail 3.
        lead (int): Leadership score.
        lead_dn1 (str): Leadership detail 1.
        lead_dn2 (str): Leadership detail 2.
        lead_dn3 (str): Leadership detail 3.
        mis (int): Mission score.
        mis_dn1 (str): Mission detail 1.
        mis_dn2 (str): Mission detail 2.
        mis_dn3 (str): Mission detail 3.
        tac (int): Tactical performance score.
        tac_dn1 (str): Tactical detail 1.
        tac_dn2 (str): Tactical detail 2.
        tac_dn3 (str): Tactical detail 3.
        recommend_1 (str): First recommendation text.
        recommend_2 (str): Second recommendation text.
        rater (str): Rater name.
        rater_date (date): Rater signature/date.
        comments_pitch (str): Short comments pitch field.
        comments (str): Full comments text.
        qualifications (str): Qualifications text field.
        promotion_recom (int): Promotion recommendation code.
        summary_rank (int): Summary rank numeric field.
        summary_sp (str): Summary SP text.
        summary_prog (str): Summary progression text.
        summary_prom (str): Summary promotion text.
        summary_mp (str): Summary MP text.
        summary_ep (str): Summary EP text.
        retention_yes (bool): Retention yes flag.
        retention_no (bool): Retention no flag.
        rsca (int): RSCA code.
        rs_address (str): Reporting senior address (combined).
        rs_address1 (str): Reporting senior address line 1.
        rs_address2 (str): Reporting senior address line 2.
        rs_city (str): Reporting senior city.
        rs_state (str): Reporting senior state.
        rs_zip_cd (str): Reporting senior ZIP code.
        rs_phone (str): Reporting senior phone number.
        rs_dsn (str): Reporting senior DSN number.
        senior_rater (str): Senior rater name.
        senior_rater_date (date): Senior rater signature/date.
        statement_yes (bool): Statement yes flag.
        statement_no (bool): Statement no flag.
        rs_info (str): Reporting senior additional info.
        rrs_fi (str): RRS first initial.
        rrs_mi (str): RRS middle initial.
        rrs_last_name (str): RRS last name.
        rrs_grade (str): RRS grade.
        rrs_command (str): RRS command.
        rrs_uic (str): RRS UIC.
        user_comments (str): User-provided comments.
        psswrd (str): Password or protection field.
        standards (str): Standards text field.
        is_validated (str): Validation status flag or note.
    """

    report_id: int = Field(primary_key=True)
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
