from datetime import date

import pytest
from sqlmodel import Session, create_engine, select
from typer.testing import CliRunner

from navfitx.cli import app
from navfitx.importer import (
    ImportSchemaError,
    build_chiefeval_template_toml,
    build_eval_template_toml,
    build_fitrep_template_toml,
    parse_report_toml,
)
from navfitx.models import ChiefEval, Eval, Fitrep

runner = CliRunner()


def test_parse_report_toml_accepts_header_only_draft() -> None:
    report = parse_report_toml('schema_version = 1\ndoc_type = "fitrep"\n')

    assert isinstance(report, Fitrep)
    assert report.doc_type == "fitrep"


def test_parse_report_toml_accepts_chiefeval_header_only_draft() -> None:
    report = parse_report_toml('schema_version = 1\ndoc_type = "chiefeval"\n')

    assert isinstance(report, ChiefEval)
    assert report.doc_type == "chiefeval"


def test_parse_report_toml_accepts_eval_header_only_draft() -> None:
    report = parse_report_toml('schema_version = 1\ndoc_type = "eval"\n')

    assert isinstance(report, Eval)
    assert report.doc_type == "eval"


def test_parse_report_toml_rejects_unknown_keys() -> None:
    with pytest.raises(ImportSchemaError, match="Unknown key"):
        parse_report_toml('schema_version = 1\ndoc_type = "fitrep"\nmade_up = "x"\n')


def test_parse_report_toml_rejects_id_key() -> None:
    with pytest.raises(ImportSchemaError, match="Unknown key"):
        parse_report_toml('schema_version = 1\ndoc_type = "fitrep"\nid = 1\n')


def test_parse_report_toml_rejects_missing_import_header() -> None:
    with pytest.raises(ImportSchemaError, match="schema_version"):
        parse_report_toml('doc_type = "fitrep"\n')


def test_parse_report_toml_rejects_missing_doc_type_header() -> None:
    with pytest.raises(ImportSchemaError, match="doc_type"):
        parse_report_toml("schema_version = 1\n")


def test_parse_report_toml_coerces_uppercase_eval_doc_type_in_draft_mode() -> None:
    report = parse_report_toml('schema_version = 1\ndoc_type = "EVAL"\n')

    assert isinstance(report, Eval)
    assert report.doc_type == "eval"


def test_parse_report_toml_strict_rejects_uppercase_eval_doc_type() -> None:
    with pytest.raises(ImportSchemaError, match="Unsupported doc_type"):
        parse_report_toml('schema_version = 1\ndoc_type = "EVAL"\n', strict=True)


def test_parse_report_toml_coerces_legacy_shape_in_draft_mode() -> None:
    report = parse_report_toml(
        "\n".join(
            [
                'schema_version = "1"',
                'doc_type = "FITREP"',
                'periodic = "true"',
                'trait1 = "3"',
                'date_reported = "2025-02-01"',
            ]
        )
        + "\n"
    )

    assert report.doc_type == "fitrep"
    assert report.periodic is True
    assert report.trait1 == 3
    assert report.date_reported == date(2025, 2, 1)


def test_parse_report_toml_strict_mode_rejects_legacy_bool() -> None:
    with pytest.raises(ImportSchemaError, match="periodic"):
        parse_report_toml('schema_version = 1\ndoc_type = "fitrep"\nperiodic = "true"\n', strict=True)


def test_parse_report_toml_coerces_lowercase_enum_tokens_in_draft_mode() -> None:
    report = parse_report_toml(
        "\n".join(
            [
                "schema_version = 1",
                'doc_type = "fitrep"',
                'group = "act"',
                'promotion_status = "regular"',
                'billet_subcategory = "na"',
            ]
        )
        + "\n"
    )

    assert report.group is not None
    assert report.promotion_status is not None
    assert report.billet_subcategory is not None
    assert report.group.value == "ACT"
    assert report.promotion_status.value == "REGULAR"
    assert report.billet_subcategory.value == "NA"


def test_parse_report_toml_strict_rejects_boolean_schema_version() -> None:
    with pytest.raises(ImportSchemaError, match="schema_version"):
        parse_report_toml('schema_version = true\ndoc_type = "fitrep"\n', strict=True)


def test_parse_report_toml_strict_rejects_boolean_trait() -> None:
    with pytest.raises(ImportSchemaError, match="trait1"):
        parse_report_toml('schema_version = 1\ndoc_type = "fitrep"\ntrait1 = true\n', strict=True)


def test_parse_report_toml_rejects_nested_table_values() -> None:
    with pytest.raises(ImportSchemaError, match="scalar"):
        parse_report_toml('schema_version = 1\ndoc_type = "fitrep"\n[name]\nfirst = "A"\n')


def test_parse_report_toml_strict_rejects_toml_datetime_for_date_fields() -> None:
    with pytest.raises(ImportSchemaError, match="date_reported"):
        parse_report_toml(
            'schema_version = 1\ndoc_type = "fitrep"\ndate_reported = 2025-02-01T10:00:00Z\n',
            strict=True,
        )


def test_parse_report_toml_accepts_multiline_strings() -> None:
    report = parse_report_toml('schema_version = 1\ndoc_type = "fitrep"\ncomments = """Line one\n\nLine two"""\n')

    assert report.comments == "Line one\n\nLine two"


def test_cli_import_adds_report_to_database(tmp_path) -> None:
    db_path = tmp_path / "navfitx.db"
    input_path = tmp_path / "report.toml"
    input_path.write_text('schema_version = 1\ndoc_type = "fitrep"\n', encoding="utf-8")

    result = runner.invoke(
        app,
        [
            "import",
            "--input",
            str(input_path),
            "--db",
            str(db_path),
        ],
    )

    assert result.exit_code == 0

    report_count = 0
    with Session(create_engine(f"sqlite:///{db_path}")) as session:
        report_count = len(session.exec(select(Fitrep)).all())

    assert report_count == 1


def test_cli_import_adds_chiefeval_to_database(tmp_path) -> None:
    db_path = tmp_path / "navfitx.db"
    input_path = tmp_path / "report.toml"
    input_path.write_text('schema_version = 1\ndoc_type = "chiefeval"\n', encoding="utf-8")

    result = runner.invoke(
        app,
        [
            "import",
            "--input",
            str(input_path),
            "--db",
            str(db_path),
        ],
    )

    assert result.exit_code == 0

    report_count = 0
    with Session(create_engine(f"sqlite:///{db_path}")) as session:
        report_count = len(session.exec(select(ChiefEval)).all())

    assert report_count == 1


def test_cli_import_adds_eval_to_database(tmp_path) -> None:
    db_path = tmp_path / "navfitx.db"
    input_path = tmp_path / "report.toml"
    input_path.write_text('schema_version = 1\ndoc_type = "eval"\n', encoding="utf-8")

    result = runner.invoke(
        app,
        [
            "import",
            "--input",
            str(input_path),
            "--db",
            str(db_path),
        ],
    )

    assert result.exit_code == 0

    report_count = 0
    with Session(create_engine(f"sqlite:///{db_path}")) as session:
        report_count = len(session.exec(select(Eval)).all())

    assert report_count == 1


def test_cli_import_strict_rejects_incomplete_report(tmp_path) -> None:
    db_path = tmp_path / "navfitx.db"
    input_path = tmp_path / "report.toml"
    input_path.write_text('schema_version = 1\ndoc_type = "fitrep"\n', encoding="utf-8")

    result = runner.invoke(
        app,
        [
            "import",
            "--input",
            str(input_path),
            "--db",
            str(db_path),
            "--strict",
        ],
    )

    assert result.exit_code == 1
    assert "Report date must be set" in result.stdout


def test_cli_import_strict_rejects_incomplete_chiefeval(tmp_path) -> None:
    db_path = tmp_path / "navfitx.db"
    input_path = tmp_path / "report.toml"
    input_path.write_text('schema_version = 1\ndoc_type = "chiefeval"\n', encoding="utf-8")

    result = runner.invoke(
        app,
        [
            "import",
            "--input",
            str(input_path),
            "--db",
            str(db_path),
            "--strict",
        ],
    )

    assert result.exit_code == 1
    assert "Report date must be set" in result.stdout


def test_cli_import_strict_rejects_incomplete_eval(tmp_path) -> None:
    db_path = tmp_path / "navfitx.db"
    input_path = tmp_path / "report.toml"
    input_path.write_text('schema_version = 1\ndoc_type = "eval"\n', encoding="utf-8")

    result = runner.invoke(
        app,
        [
            "import",
            "--input",
            str(input_path),
            "--db",
            str(db_path),
            "--strict",
        ],
    )

    assert result.exit_code == 1
    assert "Report date must be set" in result.stdout


def test_build_fitrep_template_toml_has_import_header_and_all_keys() -> None:
    template = build_fitrep_template_toml()
    parsed = parse_report_toml(template)

    assert parsed.doc_type == "fitrep"
    assert "schema_version = 1" in template

    for key in Fitrep.model_fields:
        if key in {"id", "doc_type"}:
            continue
        assert f"{key} = " in template


def test_build_chiefeval_template_toml_has_import_header_and_all_keys() -> None:
    template = build_chiefeval_template_toml()
    parsed = parse_report_toml(template)

    assert isinstance(parsed, ChiefEval)
    assert parsed.doc_type == "chiefeval"
    assert "schema_version = 1" in template

    for key in ChiefEval.model_fields:
        if key in {"id", "doc_type"}:
            continue
        assert f"{key} = " in template


def test_build_eval_template_toml_has_import_header_and_all_keys() -> None:
    template = build_eval_template_toml()
    parsed = parse_report_toml(template)

    assert isinstance(parsed, Eval)
    assert parsed.doc_type == "eval"
    assert "schema_version = 1" in template

    for key in Eval.model_fields:
        if key in {"id", "doc_type"}:
            continue
        assert f"{key} = " in template
