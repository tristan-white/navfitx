# NAVFITX

NAVFITX is a drop-in replacement for NAVFIT98A.

See [here](./docs/navfitx.pdf) for more information about why NAVFIT98 needs to be replaced.

> Note:
> NAVFITX is still in production.

| Feature | NAVFIT98A v33 | NAVFITX | 
|---------|---------------|---------|
| Export Reports as PDF | ✅ | ✅ |
| Runs on Windows 7 | ❌ | ❌ |
| Cross-Platform (Windows/MacOS/Linux) | ❌ | ✅ |
| Install & Use w/out Admin Privileges | ❌ | ✅ |
| Open Source | ❌ | ✅ |

## Installation

NAVFITX uses [uv](https://docs.astral.sh/uv/) to manage dependencies.

1. [Install uv](https://docs.astral.sh/uv/getting-started/installation/).
2. `git clone https://github.com/tristan-white/navfitx.git && cd navfitx`
3. `uv sync`
4. `uv run python -m navfitx`

> NOTE:
> If you see the error `This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.`, install `libxcb-cursor0`, then run again.
> If you see the error `ImportError: libodbc.so.2: cannot open shared object file: No such file or directory`, install unixodbc: `sudo apt install unixodbc`.
 

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
