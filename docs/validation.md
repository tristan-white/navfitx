# Validation

This page contains validation constraints that fields in performance evaluation reports must conform to in accordance with the [EVALMAN](https://www.mynavyhr.navy.mil/Portals/55/Reference/Instructions/BUPERS/BUPERSINST%201610.10.pdf?ver=g42WV7fkucvkkZolLrWseA%3d%3d).

## All Reports

### Name

- Limit of 27 characters

### Rate

- Limit of 5 characters.

### Desig

- Limit of 12 characters.

### SSN

- Must consist of 9 digits with hyphens in the format XXX-XX-XXXX

### Group

- Only one box can contain an X

### UIC

- Cannot be blank.
- Max length of 5 characters.

### Station

- Max length of 18 characters.

### Promotion Status

### Date Reported

- Cannot be blank.
- Date must be in the `YYMMMDD` format (eg: 01 January, 2000 -> 00JAN01).
- Cannot be after [Date Counseled](#date-counseled).
- Cannot be after [Period Start](#period-start)
- Cannot be after [Period End](#period-end)

### Periodic

### Detachment of Individual

- Cannot be marked if the `Special` Occasion for Report is marked.

### Special

- Cannot be marked if any of the other Occasions for Report are marked.

### Period Start

- Cannot be blank.
- Date must be in the `YYMMMDD` format (eg: 01 January, 2000 -> 00JAN01).
- Cannot be before [Date Reported](#date-reported).
- Cannot be after [Date Counseled](#date-counseled).
- Cannot be after [Period End](#period-end)

### Period End

- Cannot be blank.
- Date must be in the `YYMMMDD` format (eg: 01 January, 2000 -> 00JAN01).
- Cannot be before [Date Reported](#date-reported).
- Cannot be before [Date Counseled](#date-counseled).
- Cannot be before [Period Start](#period-start)

### Not Observed

- NOB reports are suitable for periods over 10 days, whereas periods under 10 days may be assessed by a performance information memorandum (PIM) per chapter 12 of EVALMAN.

!!! note "Observed Report with Not-Observed Traits or Promotion Recommendation"
    When circumstances warrant, it is allowable to evaluate a maximum of three traits without making a promotion recommendation. In such cases, leave the "Not Observed Report" block blank and submit an Observed report. Grade up to three traits and mark all other traits and the promotion recommendation as "NOB." Leave the promotion recommendation summary blank and make any career recommendations deemed appropriate. State the reason for not making a promotion recommendation and make comments on the three graded traits in the block for Comments on Performance. All traits graded will be added to the reporting senior’s cumulative average. An Observed report with an “NOB” promotion recommendation cannot be submitted if the member receives a 1.0 in any trait, a single 2.0 or below in Command or Organizational Climate/Equal Opportunity or Character, three 2.0 trait grades, or adverse information in the comments

### Regular

### Concurrent

### Billet Subcategory

- Must be one of the following values: 'NA', 'BASIC', 'APPROVED', 'CO AFLOAT', 'CO ASHORE', 'OIC', 'INDIV AUG', 'SEA COMP', 'CRF', 'CANVASSER', 'RESIDENT', 'INTERN', 'INSTRUCTOR', 'STUDENT', 'RESAC1', 'RESAC 6', 'SPECIAL01' through 'SPECIAL20'.

!!! note
    Users must have CNPC approval to use one of the “Special” subcategories.

### Senior Name

- Limit of 27 characters.

### Senior Grade

- Limit of 5 characters.

### Senior Title

- Limit of 14 characters.

### Senior UIC

- Limit of 5 characters.

### Senior SSN

- Must consist of 9 digits with hyphens in the format XXX-XX-XXXX

### Command Employment and Command Achievements



### Duties Abbreviation

### Duties Description

### Date Counseled

### Counselor

### Career Recommendation 1

- Must be blank if report is [NOB](#not-observed)

## FITREPs

### Detachment of Reporting Senior

- Cannot be marked if the `Special` Occasion for Report is marked.

## CHIEFEVALs

## EVALs