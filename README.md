# NAVFITX

NAVFITX is a drop-in replacement for NAVFIT98A.

> [!NOTE]
> NAVFITX is still in production.

| Feature | NAVFIT98A v33 | NAVFITX | 
|---------|---------------|---------|
| Export Reports as PDF | :white_check_mark: | :white_check_mark: |
| Runs on Windows 7 | :x: | :x: |
| Cross-Platform (Windows/MacOS/Linux) | :x: | :white_check_mark: |
| Install & Use w/out Admin Privileges | :x: | :white_check_mark: |
| Open Source | :x: | :white_check_mark: |
<!-- | Imports Microsoft Access Databases (.accdb) | :white_check_mark: | :white_check_mark: | -->

## Installation

NAVFITX uses [uv](https://docs.astral.sh/uv/) to manage dependencies.

1. [Install uv](https://docs.astral.sh/uv/getting-started/installation/).
2. `git clone https://github.com/tristan-white/navfitx.git && cd navfitx`
3. `uv sync`
4. `uv run python -m navfitx`

> [!NOTE]
> If you see the error `This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.`, install `libxcb-cursor0`, then run again.
> If you see the error `ImportError: libodbc.so.2: cannot open shared object file: No such file or directory`, install unixodbc: `sudo apt install unixodbc`.
 

## Background

- Every year, every service member in the Navy creates a performance evalution report.
- Each report is a single, two-sided PDF document. Reports are submitted physically via mail it to NAVPERSCOM.[^2]
- NAVFIT98A was released in 1998. It was/is a Windows GUI application written in Visual Basic that allows users to electronically create an edit reports.
- NAVFIT98A did not receive any major update for over [two decades](https://blog.usni.org/posts/2018/10/11/happy-anniversary-navfit98). It became evident that a more modern solution was needed.
- In 2022, the Navy released eNavFit, which was "designed to be a bridge to future performance evaluation modernization".[^3]
- eNavFit encountered so many bugs and issues during its rollout that in November 2023, the Navy released [NAVADMIN 279/23](https://navadmin-viewer.fly.dev/NAVADMIN/279/23), stating that NAVFIT98A would continue to be available through the end of 2025 while problems with eNavFit were fixed.
- In January 2025, [NAVADMIN 012/25](https://www.mynavyhr.navy.mil/Portals/55/Messages/NAVADMIN/NAV2025/NAV25012.pdf?ver=XNxecwkcKmyF0dFjhYHpzA%3d%3d) was released, stating that eNavFit would no longer available for use starting 1 May 2025. Furthermore, it anounced a "modernized and more capable NAVFIT98A" update to be released that month, providing service members with a more "user-friendly" experience, along with "updated business rules that will significantly reduce the number of rejected reports received by Navy Personnel Command".[^4]

## Why replace NAVFIT98A?

![NAVFIT98A v33](./docs/img/navfit98a_v33.png)
*NAVFIT98A Version 33, up-to-date as of this writing in October 2025.*

The need for a platform that can easily facilitate the creation, revision, validation, and submission of performance evaluations is a real one. The Navy recognized this fact which led to the effort to create eNavFit. When eNavFit failed, version 33 of NAVFIT98A was released. It offered nomianl improvements, but many of the same issues remain:

- **Installation is difficult.** NAVFIT98A is not a self-contained executable. It requires dependencies that must be installed separately. Addtionally, according to the user guide, it can require both admin privileges for the host and admin privileges for the Windows Domain in order to install.
- **It's buggy.** When it does throw an error, the error messages do not give helpful info about what went wrong.
- **It's still hard to collaborate on reports.** Before a report is fully ready to be printed as a PDF, it's common for sailors to collaborate with their chain of command, department, and/or admin department on the contents of their report. Unfortunately, the only export format for NAVFIT98A is as a Microsoft Access Database (`.accdb`) file. Using this format is quite limiting, as the contents can only be viewed inside NAVFIT98A.[^5] To make the problem worse, if you try to import `.accdb` files exported from earlier versions of NAVFIT98A into NAVFTI98A v33, you'll get an error with no message as to what went wrong.
- **It's not intuitive to use.** There are multiple official user guides and FAQs PDFs, and despite these, over 50,000 reports a year submitted to NAVPERSCOM are rejected for incorrectness. 

## Links

- [NAVFIT98A v30 User Guide Manual](https://www.mynavyhr.navy.mil/Portals/55/Career/PerformanceEvaluation/NAVFIT98A%20Version%2030%20user%20guide.pdf?ver=rBFhxjABpJhUybBeMo6AMA%3d%3d)
- [Performance Evaluation Links](https://www.mn3p.navy.mil/web/performance/overview)

## Feedback

I'd like to see NAVFITX replace NAFIT98A in the fleet. I'm looking for user testimonials from anyone that's used NAVFIT98A or eNavFit in order to answer the "why is this important" when I make the pitch to stakeholders within the Navy. If you have feedback on these programs, please provide it here:

- [Provide feedback on NAVFIT98A](https://github.com/tristan-white/navfitx/discussions/1)
- [Provide feedback on eNavFit](https://github.com/tristan-white/navfitx/discussions/2) (if you had the chance to use it before it was shut down)

---

[^1]: Even in 2025, evaluation reports are still submitted on physical paper via snailmail to Navy Personnel Command; [Performance Evaluation Reports Frequently Asked Questions August 2025](https://www.mn3p.navy.mil/documents/d/performance/navfit98a-v2-2-0-33-frequently-asked-question?download=true) states: "Presently, there is no electronic system to submit performance evaluation reports. Per BUPERSINST 1610.10H, chapter 1, paragraph 1-5, All reports must be mailed within 15 days of the ending date (block 15) for active-duty members and within 30 days for INACT members."
[^2]: [BUPERSINT 1610.10H](https://www.mynavyhr.navy.mil/Portals/55/Reference/Instructions/BUPERS/BUPERSINST%201610.10.pdf?ver=DZVcHnNH8gLkDjKjDFyaKA%3d%3d) - This document provides policy and procedures for the Navy Performance Evaluation System. It has comprehensive insructions for how to complete and submit reports.
[^3]: [NAVADMIN 279/23](https://navadmin-viewer.fly.dev/NAVADMIN/279/23) - Permitted NAVFIT98A to be used through the end of 2025 due to issues with eNavFit.
[^4]: [NAVADMIN 012/25](https://www.mynavyhr.navy.mil/Portals/55/Messages/NAVADMIN/NAV2025/NAV25012.pdf?ver=XNxecwkcKmyF0dFjhYHpzA%3d%3d) - Announced eNavFit would be scrapped, and NAVFIT98A version 32 release.
[^5]: You can also of course open the file using [Microsoft Access](https://www.microsoft.com/en-us/microsoft-365/access), but 1) many people don't know this 2) it's only available for Windows 3) it's not installed on many of the workstations where NAVFIT98A is installed.
