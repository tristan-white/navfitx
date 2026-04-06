'''

def create_eval_pdf(eval: Fitrep, path: Path) -> None:
    """Fills out a eval PDF report with the provided eval data."""
    blank_eval = get_blank_report_path("eval")
    doc = pymupdf.open(str(blank_eval))
    meta = doc.metadata
    meta["title"] = f"eval for {eval.name}"
    doc.set_metadata(meta)
    front = doc[0]
    back = doc[1]
    front.insert_text(Point(22, 43), eval.name, fontsize=12, fontname="cour")
    back.insert_text(Point(22, 43), eval.name, fontsize=12, fontname="Cour")
    front.insert_text(Point(292, 43), eval.grade, fontsize=12, fontname="Cour")
    back.insert_text(Point(292, 43), eval.grade, fontsize=12, fontname="Cour")
    front.insert_text(Point(360, 43), eval.desig, fontsize=12, fontname="Cour")
    back.insert_text(Point(360, 43), eval.desig, fontsize=12, fontname="Cour")
    front.insert_text(Point(460, 43), eval.ssn, fontsize=12, fontname="Cour")
    back.insert_text(Point(460, 43), eval.ssn, fontsize=12, fontname="Cour")
    if group_point := get_group_point(eval):
        front.insert_text(group_point, "X", fontsize=12, fontname="Cour")
    front.insert_text(Point(170, 67), eval.uic, fontsize=12, fontname="Cour")
    front.insert_text(Point(223, 67), eval.station, fontsize=12, fontname="Cour")
    front.insert_text(Point(416, 67), eval.promotion_status, fontsize=12, fontname="Cour")
    report_date_str = format_date(eval.date_reported)
    front.insert_text(Point(496, 67), report_date_str, fontsize=12, fontname="Cour")

    for point in get_occasion_points(eval):
        front.insert_text(point, "X", fontsize=12, fontname="Cour")

    from_date_str = format_date(eval.period_start)
    front.insert_text(Point(395, 92), from_date_str, fontsize=12, fontname="Cour")
    to_date_str = format_date(eval.period_end)
    front.insert_text(Point(494, 92), to_date_str, fontsize=12, fontname="Cour")
    if eval.not_observed:
        front.insert_text(Point(77, 112), "X", fontsize=12, fontname="Cour")

    # TODO: add logic for block 17-19
    # front.insert_text(Point(156, 112), "X", fontsize=12, fontname="Cour")

    front.insert_text(Point(361, 115), eval.physical_readiness, fontsize=12, fontname="Cour")
    front.insert_text(Point(460, 115), eval.billet_subcategory, fontsize=12, fontname="Cour")

    front.insert_text(Point(22, 140), eval.senior_name, fontsize=12, fontname="Cour")
    front.insert_text(Point(172, 140), eval.senior_grade, fontsize=12, fontname="Cour")
    front.insert_text(Point(222, 140), eval.senior_desig, fontsize=12, fontname="Cour")
    front.insert_text(Point(273, 140), eval.senior_title, fontsize=12, fontname="Cour")
    front.insert_text(Point(405, 140), eval.senior_uic, fontsize=12, fontname="Cour")
    front.insert_text(Point(461, 140), eval.senior_ssn, fontsize=12, fontname="Cour")

    front.insert_text(Point(24, 164), format_job(eval.job), fontsize=10, fontname="Cour", lineheight=1.0)
    front.insert_text(Point(28, 212), eval.duties_abbreviation, fontsize=12, fontname="Cour")

    duties_desc = wrap_duty_desc(eval.duties_description)
    front.insert_text(Point(24, 212), duties_desc, fontsize=10, fontname="Cour", lineheight=1.0)

    for point in get_perfomance_points(eval):
        front.insert_text(point, "X", fontsize=12, fontname="Cour")

    counsel_date_str = format_date(eval.date_counseled)
    front.insert_text(Point(200, 272), counsel_date_str, fontsize=12, fontname="Cour")

    front.insert_text(Point(279, 272), eval.counselor, fontsize=12, fontname="Cour")

    for point in get_perf_points_back(eval):
        back.insert_text(point, "X", fontsize=12, fontname="Cour")

    back.insert_text(
        Point(34, 354),
        eval.wrap_text(eval.comments, 92),
        fontsize=9.2,
        fontname="Cour",
    )

    if eval.indiv_promo_rec is not None:
        back.insert_text(get_promo_rec_point(eval), "X", fontsize=12, fontname="Cour")

    back.insert_text(Point(388, 586), eval.senior_address, fontsize=9, fontname="Cour", lineheight=1.1)
    back.insert_text(Point(105, 694), eval.member_trait_avg(), fontsize=12, fontname="Cour")
    back.insert_text(Point(240, 694), eval.summary_group_avg(), fontsize=12, fontname="Cour")
    back.insert_text(Point(370, 300), textwrap.fill(eval.career_rec_1, 13), fontsize=10, fontname="Cour")
    back.insert_text(Point(467, 300), textwrap.fill(eval.career_rec_2, 13), fontsize=10, fontname="Cour")

    doc.save(str(path))
    doc.close()

'''
