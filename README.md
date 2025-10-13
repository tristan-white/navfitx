# NAVFITX

NAVFITX is a next-gen, drop-in replacement for NAVFIT98A.

## Background

- Every year, every service member in the Navy creates a performance evalution report.
- Each report is a single, two-sided PDF document. Reports are submitted physically via mail it to NAVPERSCOM.[^2]
- NAVFIT98A was released in 1998. It was/is a Windows GUI application written in Visual Basic that allows users to electronically create an edit reports.
- NAVFIT98A did not receive any major update for over [two decades](https://blog.usni.org/posts/2018/10/11/happy-anniversary-navfit98). It became evident that a more modern solution was needed.
- In 2022, the Navy released eNavFit, which was "designed to be a bridge to future performance evaluation modernization".[^3]
- eNavFit encountered so many bugs and issues during its rollout that in November 2023, the Navy released [NAVADMIN 279/23](https://navadmin-viewer.fly.dev/NAVADMIN/279/23), stating that NAVFIT98A would continue to be available through the end of 2025 while problems with eNavFit were fixed.
- In January 2025, [NAVADMIN 012/25](https://www.mynavyhr.navy.mil/Portals/55/Messages/NAVADMIN/NAV2025/NAV25012.pdf?ver=XNxecwkcKmyF0dFjhYHpzA%3d%3d) was released, stating that eNavFit would no longer available for use starting 1 May 2025. Furthermore, it anounced a "modernized and more capable NAVFIT98A" update to be released that month, providing service members with a more "user-friendly" experience, along with "updated business rules that will significantly reduce the number of rejected reports received by Navy Personnel Command".[^4]

## Current State of NAVFIT98A

<figure style="width: 700px; text-align: center;">
  <picture>
    <img src="./docs/img/navfit98a_v33.png" alt="NAVFIT98A v33" style="width: 100%;">
  </picture>
  <figcaption>NAVFIT98A Version 33; up-to-date as of this writing in October 2025</figcaption>
</figure>

When [NAVADMIN 012/25](https://www.mynavyhr.navy.mil/Portals/55/Messages/NAVADMIN/NAV2025/NAV25012.pdf?ver=XNxecwkcKmyF0dFjhYHpzA%3d%3d) was released in Jan 2025, the new version 32 update had not yet been released. As of this writing (Oct 2025), NAVFIT98A is now on version 33, and the Navy has not anounced any plans to move away from NAVFIT98A going forward.

The need for a platform that can easily facilitate the creation, revision, validation, and submission of performance evaluations is a real one. The Navy recognized this fact when it attempted to roll out eNavFit. The most recent update offers nomianl improvements, but many of the same issues remain:

- Installation triggers Microsoft Defender Antivirus alerts because its software is so antiquated.
- It's very buggy. It's prone to crashing, or throwing errors with unhelpful error messages that do not make it clear what went wrong.
- bad output formats
- poor user guide / installation instructions
- What you see is not what you get
- It isn't simple to install. 
- validation could be improved even more
- not backward compatible; not all .accdb files created by NAVFIT98A can be opened by all other versions.
- not extensible

## Links

- [NAVFIT98A v30 User Guide Manual](https://www.mynavyhr.navy.mil/Portals/55/Career/PerformanceEvaluation/NAVFIT98A%20Version%2030%20user%20guide.pdf?ver=rBFhxjABpJhUybBeMo6AMA%3d%3d)
- [Performance Evaluation Links](https://www.mn3p.navy.mil/web/performance/overview)

## Roadmap

- Create PDF export template for [NAVPERS 1610/2](https://www.mynavyhr.navy.mil/Portals/55/Reference/Forms/NAVPERS/NAVPERS%201610-2%2005-2025_Final.pdf?ver=HYg5l9GDUkjIZR6sLcrvUw%3d%3d)
- Create PDF export template for [NAVPERS 1610/20](https://www.mynavyhr.navy.mil/Portals/55/Reference/Forms/NAVPERS/NAVPERS%201616-26%2005-2025_Final.pdf?ver=peRWyCZKmmrvKu6HcVXCtQ%3d%3d)
- Create PDF export template for [NAVPERS 1610/5](https://www.mynavyhr.navy.mil/Portals/55/Reference/Forms/NAVPERS/NAVPERS%201616-26%2005-2025_Final.pdf?ver=peRWyCZKmmrvKu6HcVXCtQ%3d%3d)
- [Add .toml input option](./navpers_1610-2_example.toml)
- Add .accdb file input option
- Add .accdb file output option
- Add sqlite output option
- Add sqlite input option
- Add JSON input option
- Add [FastAPI](https://fastapi.tiangolo.com/)
- Create cross-platform standalone executables with [pyinstaller](https://github.com/pyinstaller/pyinstaller)

## Support

If you're interested in seeing this project succeed, you could help in a few ways you could help:
- Give this repo a star! This helps people find the project and lets me know that you're interested in seeing it develop further.
- [Provide feedback on NAVFIT98A](https://github.com/tristan-white/navfitx/discussions/1)
- [Provide feedback on eNavFit](https://github.com/tristan-white/navfitx/discussions/2) (if you had the chance to use it before it was shut down)

[^1]: Even in 2025, evaluation reports are still submitted on physical paper via snailmail to Navy Personnel Command; [Performance Evaluation Reports Frequently Asked Questions August 2025](https://www.mn3p.navy.mil/documents/d/performance/navfit98a-v2-2-0-33-frequently-asked-question?download=true) states: "Presently, there is no electronic system to submit performance evaluation reports. Per BUPERSINST 1610.10H, chapter 1, paragraph 1-5, All reports must be mailed within 15 days of the ending date (block 15) for active-duty members and within 30 days for INACT members."
[^2]: [BUPERSINT 1610.10H](https://www.mynavyhr.navy.mil/Portals/55/Reference/Instructions/BUPERS/BUPERSINST%201610.10.pdf?ver=DZVcHnNH8gLkDjKjDFyaKA%3d%3d) - This document provides policy and procedures for the Navy Performance Evaluation System. It has comprehensive insructions for how to complete and submit reports.
[^3]: [NAVADMIN 279/23](https://navadmin-viewer.fly.dev/NAVADMIN/279/23) - Permitted NAVFIT98A to be used through the end of 2025 due to issues with eNavFit.
[^4]: [NAVADMIN 012/25](https://www.mynavyhr.navy.mil/Portals/55/Messages/NAVADMIN/NAV2025/NAV25012.pdf?ver=XNxecwkcKmyF0dFjhYHpzA%3d%3d) - Announced eNavFit would be scrapped, and NAVFIT98A version 32 release.
