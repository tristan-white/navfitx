# NAVFITX

![PyPI - Version](https://img.shields.io/pypi/v/navfitx)

NAVFITX is a feature rich, drop-in replacement for NAVFIT98A.

| Feature | NAVFIT98 v33 | NAVFITX | 
|---------|---------------|---------|
| Export Reports as PDF | ✅ | ✅ |
| Runs on Windows | ✅ | ✅ |
| Easy to install | ❌ | ✅ |
| Runs on MacOS | ❌ | ✅ |
| Runs on Linux | ❌ | ✅ |
| Install & Use w/out Admin Privileges | ❌ | ✅ |
| Export reports in a sqlite database | ❌ | ✅ |
| Export reports as JSON files | ❌ | ✅ |
| Export reports as [TOML](https://toml.io/) files | ❌ | ✅ |
| Export use via CLI | ❌ | ✅ |

## Installation

You can install and use NAVFITX in 60 seconds.

=== "Windows"

    1. Open Powershell[^1], copy/paste the following command, and hit ++enter++.

        ```
        powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
        ```

        This command installs [uv](https://docs.astral.sh/uv/), a python package manager. It makes it easy to install python packges, such as NAVFITX.

    2. Once uv has finished installing, close the Powershell window, then reopen it. 

    3. In Powershell, install and launch NAVFITX with the command `uvx navfitx`. Done!

=== "Mac / Linux"

    1. Open Terminal[^2], copy/paste the following command, and hit ++enter++.

        ```
        curl -LsSf https://astral.sh/uv/install.sh | sh
        ```

        This command installs [uv](https://docs.astral.sh/uv/), a python package manager. It makes it easy to install python packges, such as NAVFITX.

    2. Once uv has finished installing, close the Powershell window, then reopen it. 

    3. In Terminal, install and launch NAVFITX with the command `uvx navfitx`. Done!


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
