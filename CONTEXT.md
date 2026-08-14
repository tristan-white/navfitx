# NAVFITX

This context defines the canonical language used for NAVFITX report workflows and UI concepts.

## Language

**Home Page**:
The default GUI page shown after launch that hosts the Report List and top-level navigation actions.
_Avoid_: Home screen, landing screen

**Report List**:
The table on the home page that displays saved reports and allows users to browse and manage them.
_Avoid_: Reports table, home table, report grid

**Report List Fill Behavior**:
The Home Page layout behavior where the Report List occupies all remaining space below the title row and resizes with the window.
_Avoid_: Full-screen table, stretched table mode

**Report List Column Fill Mode**:
A display mode where the Report List uses available width, with high-value columns allowed to take more space while ID-style columns stay compact.
_Avoid_: Equal-stretch columns, fixed-width-only layout

**Period End**:
The ending date of a report period.
_Avoid_: To Date

**Sort State**:
The currently active sort column and sort direction used to order the Report List.
_Avoid_: Sort setting, sort preference

**Report Draft**:
A report record that may be incomplete and is still intended for further editing.
_Avoid_: Partial report, invalid report, unfinished file

**Report TOML File**:
A TOML file that stores exactly one report using the NAVFITX import schema.
_Avoid_: TOML blob, batch file, raw TOML

**Import Header**:
The minimal required keys at the top of a Report TOML File that identify schema and report type.
_Avoid_: Metadata blob, preamble

**Report Type Discriminator**:
The explicit field in a Report TOML File that declares which report type the file represents.
_Avoid_: Type hint, implicit type

**Report Type Display Name**:
The human-readable label shown in the UI for a report type, which may differ from the Report Type Discriminator.
_Avoid_: Raw doc type, internal type code

**Report Type Sort Key**:
The internal report-type value used for sorting report rows, even when the UI shows a different Report Type Display Name.
_Avoid_: Visible label sort key, inferred row sort

**Chief Evaluation**:
The report type used for chief performance assessments in NAVFITX. Its Report Type Discriminator value is `chiefeval`.
_Avoid_: Chief Eval report, CHIEFEVAL report

**Chief Eval**:
Accepted shorthand for Chief Evaluation in space-constrained UI labels.
_Avoid_: CHIEFEVAL (as user-facing label), chief report

**Import Strict Mode**:
An import mode that requires the report data to be complete and fully valid before accepting it.
_Avoid_: Hard import, safe mode

**Import Draft Mode**:
The default import mode that accepts incomplete reports for later editing.
_Avoid_: Loose mode, invalid mode

**Schema Version**:
The explicit version marker that identifies which Report TOML File schema rules apply.
_Avoid_: Format number, parser version

**Canonical TOML Value**:
The preferred representation that uses native TOML types instead of encoding all values as strings.
_Avoid_: Stringified TOML, loose value

**Legacy TOML Shape**:
An older NAVFITX TOML representation where values were exported as strings and may need compatibility coercion.
_Avoid_: Bad TOML, deprecated file

**Canonical Key Name**:
A case-sensitive schema key that matches a report model field name exactly.
_Avoid_: Alias key, display label key

**Compatibility Coercion**:
Import-time conversion of legacy TOML values into canonical typed values in draft mode.
_Avoid_: Silent rewrite, strict parsing

**Validated Example FITREP**:
A canonical sample FITREP record intended for demonstrations that satisfies strict import schema checks and complete report validation.
_Avoid_: Example report, sample fitrep, demo fitrep
