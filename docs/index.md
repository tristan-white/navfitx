# NAVFITX

NAVFITX is a drop-in replacement for NAVFIT98A.

## Installation

!!! warning
    NAVFITX is still in pre-release. Until the first minor version release (v0.1.0), updates may introduce changes that are not backward compatible.

You can install and run NAVFITX with one command.

=== "Windows"

    Open Powershell[^1], copy/paste the following command, and hit ++enter++.

    ```powershell
    powershell -ExecutionPolicy ByPass -c "irm https://uvx.sh/navfitx/install.ps1 | iex"
    ```

=== "Mac / Linux"

    Open Terminal[^2], copy/paste the following command, and hit ++enter++.

    ```sh
    curl -LsSf uvx.sh/navfitx/install.sh | sh
    ```

Installation may take up to a few minutes depending on your internet connection.

Once complete, type `navfitx` and press ++enter++ to run the program.

## Upgrading

To upgrade NAVFITX to the most recent version, run the following command in Powershell/Terminal:

```sh
uv tool install -U navfitx
```

## Help NAVFITX

#### Feedback/Suggestions

If you find a bug, have a question, or have feedback/a request for an enhancement, please create a [new issue](https://github.com/tristan-white/navfitx/issues) to track it.

#### Star NAVFITX in Github

You can "star" [NAVFITX in GitHub](https://github.com/tristan-white/navfitx) (clicking the star button at the top right).

By adding a star, other users will be able to find it more easily and see that it has already been useful for others.


[^1]: Press the ++windows++ key, then type "powershell".
[^2]: On Mac, hit ++command+space++, then type "terminal".
