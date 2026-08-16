from typer.testing import CliRunner

from navfitx.cli import app
from navfitx.examples import build_validated_example_chiefeval, build_validated_example_eval
from navfitx.importer import parse_report_toml
from navfitx.models import ChiefEval, Eval

runner = CliRunner()


def test_toml_template_chiefeval_writes_file(tmp_path) -> None:
    output = tmp_path / "chiefeval_template.toml"

    result = runner.invoke(app, ["toml", "template", "--type", "chiefeval", "--output", str(output)])

    assert result.exit_code == 0
    assert output.exists()
    parsed = parse_report_toml(output.read_text(encoding="utf-8"))
    assert isinstance(parsed, ChiefEval)
    assert parsed.doc_type == "chiefeval"


def test_toml_example_chiefeval_writes_file(tmp_path) -> None:
    output = tmp_path / "chiefeval_example.toml"

    result = runner.invoke(app, ["toml", "example", "--type", "chiefeval", "--output", str(output)])

    assert result.exit_code == 0
    assert output.exists()
    parsed = parse_report_toml(output.read_text(encoding="utf-8"))
    assert isinstance(parsed, ChiefEval)
    ChiefEval.model_validate(parsed)


def test_toml_template_eval_writes_file(tmp_path) -> None:
    output = tmp_path / "eval_template.toml"

    result = runner.invoke(app, ["toml", "template", "--type", "eval", "--output", str(output)])

    assert result.exit_code == 0
    assert output.exists()
    parsed = parse_report_toml(output.read_text(encoding="utf-8"))
    assert isinstance(parsed, Eval)
    assert parsed.doc_type == "eval"


def test_toml_example_eval_writes_file(tmp_path) -> None:
    output = tmp_path / "eval_example.toml"

    result = runner.invoke(app, ["toml", "example", "--type", "eval", "--output", str(output)])

    assert result.exit_code == 0
    assert output.exists()
    parsed = parse_report_toml(output.read_text(encoding="utf-8"))
    assert isinstance(parsed, Eval)
    Eval.model_validate(parsed)


def test_toml_pdf_requires_doc_type_header(tmp_path) -> None:
    input_path = tmp_path / "report.toml"
    output_path = tmp_path / "report.pdf"
    input_path.write_text("schema_version = 1\n", encoding="utf-8")

    result = runner.invoke(app, ["toml", "pdf", "--input", str(input_path), "--output", str(output_path)])

    assert result.exit_code == 1
    assert "Missing required import header key: doc_type" in result.stdout


def test_toml_pdf_generates_eval_pdf(tmp_path) -> None:
    input_path = tmp_path / "report.toml"
    output_path = tmp_path / "report.pdf"

    report = build_validated_example_eval()
    input_path.write_text(report.model_dump_toml(), encoding="utf-8")

    result = runner.invoke(app, ["toml", "pdf", "--input", str(input_path), "--output", str(output_path)])

    assert result.exit_code == 0
    assert output_path.exists()


def test_toml_pdf_generates_chiefeval_pdf(tmp_path) -> None:
    input_path = tmp_path / "chiefeval.toml"
    output_path = tmp_path / "chiefeval.pdf"

    report = build_validated_example_chiefeval()
    input_path.write_text(report.model_dump_toml(), encoding="utf-8")

    result = runner.invoke(app, ["toml", "pdf", "--input", str(input_path), "--output", str(output_path)])

    assert result.exit_code == 0
    assert output_path.exists()
