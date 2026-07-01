# NAVFITX

NAVFITX is a drop-in replacement for NAVFIT98A.

| Feature | NAVFIT98 v33 | NAVFITX | 
|---------|---------------|---------|
| Triggers Anti-Virus Warnings | ✅ | ❌ |
| Runs on Windows | ✅ | ✅ |
| Runs on MacOS | ❌ | ✅ |
| Runs on Linux | ❌ | ✅ |
| Export Reports as PDF | ✅ | ✅ |
| Import/export reports in a sqlite database | ❌ | ✅ |
| Install & Use w/out Admin Privileges | ❌ | ✅ |
| Easy to install | ❌ | ✅ |
| CLI tool | ❌ | ✅ |

<!-- | Import/export reports as JSON files | ❌ | ✅ |
| Import/export reports as [TOML](https://toml.io/) files | ❌ | ✅ | -->

## Quickstart

!!! note
    NAVFITX is in pre-release. Until version 0.1.0, new versions may introduce changes that are not backward compatible.

You can install and run NAVFITX with one command.

=== "Windows"

    Open Powershell[^1], copy/paste the following command, and hit ++enter++.

    ```
    powershell -ExecutionPolicy ByPass -c "irm https://uvx.sh/navfitx/install.ps1 | iex"
    ```

=== "Mac / Linux"

    Open Terminal[^2], copy/paste the following command, and hit ++enter++.

    ```
    curl -LsSf uvx.sh/navfitx/install.sh | sh
    ```

## Help NAVFITX Succeed

### Feedback/Suggestions
If you find a bug, have a question, or have feedback/a request for an enhancement, please create a [new issue](https://github.com/tristan-white/navfitx/issues) to track it.

I'd like to see NAVFITX replace NAFIT98A in the fleet. I'm looking for user testimonials from anyone that's used NAVFIT98A or eNavFit in order to answer the "why is this important" when I make the pitch to current NAVFIT98 stakeholders within the Navy. If you have feedback on these programs, please provide it here:

- [Provide feedback on NAVFIT98A](https://github.com/tristan-white/navfitx/discussions/1)
- [Provide feedback on eNavFit](https://github.com/tristan-white/navfitx/discussions/2) (if you had the chance to use it before it was shut down)

### Star NAVFITX in Github

You can "star" [NAVFITX in GitHub](https://github.com/tristan-white/navfitx) (clicking the star button at the top right).

By adding a star, other users will be able to find it more easily and see that it has already been useful for others.


[^1]: Press the ++windows++ key, then type "powershell".
[^2]: On Mac, hit ++command+space++, then type "terminal".
