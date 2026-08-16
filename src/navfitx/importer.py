import tomllib
from collections.abc import Callable
from datetime import date, datetime
from pathlib import Path
from typing import Any

import tomlkit
import typer
from pydantic import ValidationError
from rich import print
from sqlmodel import Session, SQLModel, create_engine
from typing_extensions import Annotated

from navfitx.models import BilletSubcategory, ChiefEval, DutyStatus, Fitrep, PromotionStatus

app = typer.Typer(no_args_is_help=True, add_completion=False)

SUPPORTED_SCHEMA_VERSION = 1
SUPPORTED_DOC_TYPES = {
    "fitrep",
    "chiefeval",
}
BOOL_FIELDS = {
    "periodic",
    "det_indiv",
    "special",
    "not_observed",
    "regular",
    "concurrent",
    "det_rs",
    "ops_cdr",
}
INT_FIELDS = {
    "trait1",
    "trait2",
    "trait3",
    "trait4",
    "trait5",
    "trait6",
    "trait7",
    "indiv_promo_rec",
}
DATE_FIELDS = {
    "date_reported",
    "period_start",
    "period_end",
    "date_counseled",
}
UPPERCASE_ENUM_FIELDS = {
    "group",
    "promotion_status",
    "billet_subcategory",
}
ENUM_PARSERS = {
    "group": DutyStatus,
    "promotion_status": PromotionStatus,
    "billet_subcategory": BilletSubcategory,
}


class ImportSchemaError(ValueError):
    pass


def _allowed_keys(model_type: type[Fitrep] | type[ChiefEval]) -> set[str]:
    return (set(model_type.model_fields) - {"id"}) | {"schema_version"}


def _resolve_model_type(doc_type: str) -> type[Fitrep] | type[ChiefEval]:
    if doc_type.casefold() == "eval":
        raise ImportSchemaError("EVAL CLI support is not implemented yet.")
    if doc_type == "fitrep":
        return Fitrep
    if doc_type == "chiefeval":
        return ChiefEval
    allowed = ", ".join(sorted(SUPPORTED_DOC_TYPES))
    raise ImportSchemaError(f"Unsupported doc_type: {doc_type!r}. Expected one of: {allowed}.")


def _build_report_template_toml(model_type: type[Fitrep] | type[ChiefEval], doc_type: str) -> str:
    data = model_type().model_dump(exclude={"id"})
    template_dates = {
        "date_reported": date.today(),
        "period_start": date.today(),
        "period_end": date.today(),
        "date_counseled": date.today(),
    }
    template_enums = {
        "group": "ACT",
        "promotion_status": "REGULAR",
        "billet_subcategory": "NA",
    }
    template_ints = {
        "trait1": 0,
        "trait2": 0,
        "trait3": 0,
        "trait4": 0,
        "trait5": 0,
        "trait6": 0,
        "trait7": 0,
        "indiv_promo_rec": 0,
    }

    data.update(template_dates)
    data.update(template_enums)
    data.update(template_ints)

    document = tomlkit.document()
    document.add("schema_version", SUPPORTED_SCHEMA_VERSION)
    document.add("doc_type", doc_type)
    for key in model_type.model_fields:
        if key in {"id", "doc_type"}:
            continue
        document.add(key, data[key])
    return tomlkit.dumps(document)


def build_fitrep_template_toml() -> str:
    return _build_report_template_toml(Fitrep, "fitrep")


def build_chiefeval_template_toml() -> str:
    return _build_report_template_toml(ChiefEval, "chiefeval")


def _parse_bool(value: str) -> bool:
    lowered = value.strip().lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    raise ValueError("Expected 'true' or 'false'.")


def _parse_int(value: str) -> int:
    return int(value.strip())


def _parse_date(value: str) -> date:
    return date.fromisoformat(value.strip())


def _parse_doc_type(value: str) -> str:
    return value.strip().lower()


def _coerce_legacy_string(value: str, parser: Callable[[str], Any], field_name: str) -> Any:
    try:
        return parser(value)
    except Exception as exc:
        raise ImportSchemaError(f"Invalid legacy value for '{field_name}': {value!r}") from exc


def _coerce_legacy_values(data: dict[str, Any]) -> dict[str, Any]:
    if "schema_version" in data and isinstance(data["schema_version"], str):
        data["schema_version"] = _coerce_legacy_string(data["schema_version"], _parse_int, "schema_version")
    if "doc_type" in data and isinstance(data["doc_type"], str):
        data["doc_type"] = _coerce_legacy_string(data["doc_type"], _parse_doc_type, "doc_type")

    for field_name in BOOL_FIELDS:
        if field_name in data and isinstance(data[field_name], str):
            data[field_name] = _coerce_legacy_string(data[field_name], _parse_bool, field_name)

    for field_name in INT_FIELDS:
        if field_name in data and isinstance(data[field_name], str):
            data[field_name] = _coerce_legacy_string(data[field_name], _parse_int, field_name)

    for field_name in DATE_FIELDS:
        if field_name in data and isinstance(data[field_name], str):
            data[field_name] = _coerce_legacy_string(data[field_name], _parse_date, field_name)

    for field_name in UPPERCASE_ENUM_FIELDS:
        if field_name in data and isinstance(data[field_name], str):
            data[field_name] = data[field_name].strip().upper()

    for field_name, enum_parser in ENUM_PARSERS.items():
        if field_name in data and isinstance(data[field_name], str):
            data[field_name] = _coerce_legacy_string(data[field_name], enum_parser, field_name)

    return data


def _is_int_not_bool(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _strict_type_checks(data: dict[str, Any]) -> None:
    if not _is_int_not_bool(data.get("schema_version")):
        raise ImportSchemaError("schema_version must be an integer.")
    if not isinstance(data.get("doc_type"), str):
        raise ImportSchemaError("doc_type must be a string.")

    for field_name in BOOL_FIELDS:
        if field_name in data and not isinstance(data[field_name], bool):
            raise ImportSchemaError(f"{field_name} must be a boolean.")
    for field_name in INT_FIELDS:
        if field_name in data and not _is_int_not_bool(data[field_name]):
            raise ImportSchemaError(f"{field_name} must be an integer.")
    for field_name in DATE_FIELDS:
        if field_name in data and (not isinstance(data[field_name], date) or isinstance(data[field_name], datetime)):
            raise ImportSchemaError(f"{field_name} must be a TOML date.")

    for field_name, value in data.items():
        if field_name in BOOL_FIELDS | INT_FIELDS | DATE_FIELDS | {"schema_version", "doc_type"}:
            continue
        if not isinstance(value, str):
            raise ImportSchemaError(f"{field_name} must be a string.")

    for field_name in UPPERCASE_ENUM_FIELDS:
        if field_name in data and isinstance(data[field_name], str):
            if data[field_name] != data[field_name].strip().upper():
                raise ImportSchemaError(f"{field_name} must use canonical uppercase enum tokens.")


def _reject_nested_values(data: dict[str, Any]) -> None:
    for field_name, value in data.items():
        if isinstance(value, dict | list):
            raise ImportSchemaError(f"{field_name} must be a scalar value, not a table or list.")


def _validate_header_keys(data: dict[str, Any]) -> None:
    if "schema_version" not in data:
        raise ImportSchemaError("Missing required import header key: schema_version")
    if "doc_type" not in data:
        raise ImportSchemaError("Missing required import header key: doc_type")


def _validate_header_values(data: dict[str, Any]) -> type[Fitrep] | type[ChiefEval]:
    _validate_header_keys(data)

    if data["schema_version"] != SUPPORTED_SCHEMA_VERSION:
        raise ImportSchemaError(
            f"Unsupported schema_version: {data['schema_version']!r}. Expected {SUPPORTED_SCHEMA_VERSION}."
        )
    if not isinstance(data["doc_type"], str):
        raise ImportSchemaError("doc_type must be a string.")
    return _resolve_model_type(data["doc_type"])


def parse_report_toml(toml_str: str, *, strict: bool = False, require_header: bool = True) -> Fitrep | ChiefEval:
    try:
        data = tomllib.loads(toml_str)
    except tomllib.TOMLDecodeError as exc:
        raise ImportSchemaError(f"Invalid TOML: {exc}") from exc

    if not isinstance(data, dict):
        raise ImportSchemaError("TOML root must be a key/value mapping.")

    _reject_nested_values(data)

    if not require_header:
        data.setdefault("schema_version", SUPPORTED_SCHEMA_VERSION)
        data.setdefault("doc_type", "fitrep")

    _validate_header_keys(data)

    if strict:
        _strict_type_checks(data)
    else:
        data = _coerce_legacy_values(data)

    model_type = _validate_header_values(data)

    unknown_keys = set(data) - _allowed_keys(model_type)
    if unknown_keys:
        key_list = ", ".join(sorted(unknown_keys))
        raise ImportSchemaError(f"Unknown key(s): {key_list}")

    data.pop("schema_version", None)

    if strict:
        try:
            return model_type.model_validate(data)
        except ValidationError as exc:
            raise ImportSchemaError(str(exc)) from exc
    return model_type(**data)


def import_report_toml(input_path: Path, db_path: Path, *, strict: bool = False) -> Fitrep | ChiefEval:
    try:
        toml_str = input_path.read_text(encoding="utf-8")
    except Exception as exc:
        raise ImportSchemaError(f"Unable to read TOML file: {exc}") from exc

    report = parse_report_toml(toml_str, strict=strict)

    engine = create_engine(f"sqlite:///{db_path}")
    SQLModel.metadata.create_all(engine)
    with Session(engine, expire_on_commit=False) as session:
        session.add(report)
        session.commit()
    return report


@app.command("import")
def import_command(
    input: Annotated[
        Path,
        typer.Option(
            "--input",
            "-i",
            help="Path to a NAVFITX report TOML file.",
            exists=True,
            dir_okay=False,
            readable=True,
        ),
    ],
    db: Annotated[
        Path,
        typer.Option(
            "--db",
            help="Path to the target NAVFITX SQLite database file.",
            dir_okay=False,
        ),
    ],
    strict: Annotated[
        bool,
        typer.Option(
            "--strict",
            help="Enable strict import validation (canonical TOML types and full report validation).",
        ),
    ] = False,
) -> None:
    """
    Import one report from a TOML file into a NAVFITX database.
    """
    try:
        report = import_report_toml(input, db, strict=strict)
    except ImportSchemaError as exc:
        print(f"[red]Import failed:[/red] {exc}")
        raise typer.Exit(code=1)
    except Exception as exc:
        print(f"[red]Import failed unexpectedly:[/red] {exc}")
        raise typer.Exit(code=1)

    print(f"Imported {report.doc_type} report into {db}")
