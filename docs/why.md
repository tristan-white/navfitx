# Why?

**We need a modern, secure, offline-capable replacement for NAVFIT98 to eliminate manual mailing, reduce errors, and help service members easily create reports that help their career.**

---

Since 1998, the Navy has been using a Visual Basic app called NAVFIT98 to create performance evaluation reports for all its service members. NAVFIT98 was a great step forward and made creating the performance evaluation reporting process more efficient.

But it's still being used in 2026. It has known bugs, is difficult to install, and its report validation feature is lacking, resulting in thousands[^2] of reports submitted annually that are incorrect and must be redone.

Currently, due to NAVFIT98 limitations, the only authorized method to submit reports to the Navy Personnel Command is to *physically mail them*. This means that **five to six hundred thousand** reports are physically mailed to Navy Personnel Command each year.[^2] These reports are then **manually** scanned into a Navy service members' official records.

This process is radically inefficient. But efficiency aside, there's a larger problem: since service members' reports are stored as scanned PDFs, the data therein is not queryable. Therefore, there is no programmatic method to analyze past reports and draw conclusions about the effectiveness of the Navy's Performance Evaluation system.[^1]

## eNavFit

In November 2021, the [NAVADMIN 267/21](https://www.mynavyhr.navy.mil/Portals/55/Messages/NAVADMIN/NAV2021/NAV21267.txt?ver=1m0Z1uYm9eRwZT2jHTVQLw%3D%3D) was released. It recognized the shortcomings of NAVFIT98 in its opening paragraph:

!!! quote "NAVADMIN 267/21"
    Dominance of the maritime domain requires innovation and forward thinking. With investments in platforms, weapons and technologies to meet evolving operational conditions, it is imperative that we invest in our most essential warfighting asset, our people. Talent management and modern development approaches are required to attract, develop, train and retain the best and fully qualified Sailors in our Navy.

It then announced eNavFit: a web-app intended to replace NAVFIT98. It was so bad that the Navy scrapped it:

| Date      | Event |
|-----------|-------|
| NOV2021 | [NAVADMIN 267/21](https://www.mynavyhr.navy.mil/Portals/55/Messages/NAVADMIN/NAV2021/NAV21267.txt?ver=1m0Z1uYm9eRwZT2jHTVQLw%3D%3D) announces eNavFit, a program intended to address the deficiencies with NAVFIT98 |
| JAN2022 | [NAVADMIN 004/22](https://www.mynavyhr.navy.mil/Portals/55/Messages/NAVADMIN/NAV2022/NAV22004.txt?ver=VHggr8Z2gf5-0-iI2Vo1dg%3D%3D) announces plans to sunset NAVFIT98 in late FY 2022 |
| FEB2022 | eNavFit goes online |
| NOV2022 | [NAVADMIN 250/22](https://www.mynavyhr.navy.mil/Portals/55/Messages/NAVADMIN/NAV2022/NAV22250.txt?ver=ajI0gm_W8wNT4xP0XTw9Vg%3D%3D) acknowledges issues and bugs with eNavFit and pushes NAVFIT98 sunset date back to DEC2023 |
| NOV2023 | [NAVADMIN 279/23](https://www.mynavyhr.navy.mil/Portals/55/Messages/NAVADMIN/NAV2023/NAV23279.txt?ver=RmNweMI-Qj899te0YFkGZA%3D%3D) acknowledges continued issues with eNavFit, pushing NAVFIT98 sunset date back to DEC2025 |
| JAN2025 | [NAVADMIN 012/25](https://www.mynavyhr.navy.mil/Portals/55/Messages/NAVADMIN/NAV2025/NAV25012.pdf?ver=XNxecwkcKmyF0dFjhYHpzA%3D%3D) recognizes the failure of eNavFit, and mandates NAVFIT98 return to fleet wide used by MAY2025 |
| MAY2025 | eNavFit goes offline |

### What went wrong?

- **Poor offline functionality.** eNavFit didn't work well when it wasn't internet connected. This was a non-starter for many users at sea.
- **Lack of Training.** Sailors reported that eNavFit was unnecessarily complicated and they didn’t receive adequate training to use it.
- **Poor Feedback Loops.** Sailors did not have a good mechanism for giving feed back on eNavFit deficiencies, and updates to fix bugs were very slow to be released.

## The Way Forward

To avoid the issues faced by eNavFit, a next generation NAVFIT app should have the following features:

- **Offline Capability.** This is non-negotiable.
    - NAVFITX works great offline!
- **Intuitive to Use.** It shouldn't be necessary to receive training just to create a performance evaluation report. The user experience should be intuitive and easy to use.
    - NAVFITX purposefully mimics the NAVFIT98A graphical user interface (GUI) so that NAVFIT98 users will find its use and intuitive.
- **Short Feedback Loop.** eNavFit didn't have a good mechanism for users to submit feedback, resulting in bugs that were evident to users but not always the developers. The next NAVFIT app should provide users and accessible way to let developers know about issues so that patches and updates can be rolled out quickly.
    - NAVFITX is open source. Any user can [submit issues](https://github.com/tristan-white/navfitx/issues) to the project, or even submit code to fix/add features.
- **Online Submissions.** There's no reason why a NAVFIT app shouldn't be able to submit reports to Navy Personnel Command instantly and securely over the internet. When the internet is available, this should be the primary method of submission. This would reduce the time from report completion to the time of upload into a service members' official record from weeks to seconds.

## Further Reading

- [Successful Practices for Employee Performance Evaluations](https://apps.dtic.mil/sti/citations/AD1114373)
- [Improving the Navy’s Performance Evaluation System with Successful Practices](https://dair.nps.edu/handle/123456789/4730)
- [Military Officer Performance: Actions Needed to Fully Incorporate Performance Evaluation Key Practices](https://www.gao.gov/assets/gao-25-106618.pdf)

[^1]: This problem is summarized well by Laura Small from the Naval Postgraduate School in her thesis [*Successful Practices for Employee Performance Evaluations*](https://apps.dtic.mil/sti/citations/AD1114373); see section III.D: "FINDINGS: CURRENT PES SHORTCOMINGS".
[^2]: [Performance Evaluation FAQ](https://www.mynavyhr.navy.mil/Career-Management/Performance-Evaluation/FAQ/)
