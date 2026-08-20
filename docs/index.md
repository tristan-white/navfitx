# NAVFITX

NAVFITX is a replacement for NAVFIT98A.

It fixes [problems with NAVFIT98](why.md). See [Feature Parity](#feature-parity) for a list of current and future NAVFITX features.

??? warning "NAVFITX is in pre-release"
    Until the first minor version release (v0.1.0), updates may introduce changes that are not backward compatible.

## Installation

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

## Feature Parity

NAVFITX aims to be a feature rich drop-in replacement for NAVFIT98; ie, an app that that has all of NAVFIT98's functionality and more so that you can seamlessly switch to NAVFITX today.

NAVFITX is actively being developed and has not yet reached full feature parity. The following list tracks which features are already available in NAVFITX and which are still being developed.

---

:lucide-circle-check-big:{ .checked } Generate EVAL PDFs

:lucide-circle-check-big:{ .checked } Generate FITREP PDFs

:lucide-circle: Generate CHIEFEVAL PDFs

:lucide-circle: Import NAVFIT98 `.accdb` Microsoft Access Database files[^3]

:lucide-circle-check-big:{ .checked } Validate Reports[^4]

:lucide-circle: Report Templates (called "Folders" in NAVFIT98)

:lucide-circle: Generate Summary Letter PDFs

## Help NAVFITX

#### Feedback/Suggestions

If you find a bug, have a question, or have feedback/a request for an enhancement, please create a [new issue](https://github.com/tristan-white/navfitx/issues) to track it.

#### Star NAVFITX in Github

You can "star" [NAVFITX in GitHub](https://github.com/tristan-white/navfitx) (clicking the star button at the top right).

By adding a star, other users will be able to find it more easily and see that it has already been useful for others.


[^1]: Press the ++windows++ key, then type "powershell".
[^2]: On Mac, hit ++command+space++, then type "terminal".
[^3]: NAVFITX uses SQLite databases. A future release will allow it to read database files generated from NAVFIT98 so that you can import your NAVFIT98 database into NAVFITX.
[^4]: NAVFIT98 validation checks are not complete; reports that pass NAVFIT98 validation are not guaranteed to conform to [BUPERSINST 1610.10H](https://www.mynavyhr.navy.mil/Portals/55/Reference/Instructions/BUPERS/BUPERSINST%201610.10.pdf?ver=g42WV7fkucvkkZolLrWseA%3d%3d). NAVFITX does a lot more validation. It's not yet guaranteed to match BUPERSINST 1610.10H, but it guaranteed to do better/more complete validation than NAVFIT98.
