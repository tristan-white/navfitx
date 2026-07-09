# Contributing

## Dev Environment

### Virtual Environment / Dependency Setup

NAVFITX uses [uv](https://docs.astral.sh/uv/) for package management. See the [uv documentation](https://docs.astral.sh/uv/) for info on how to manage python virtual environments and dependencies with uv. 

### Pre-commit

[Pre-commit](https://pre-commit.com/) is used to ensure all pushed code is linted, formatted, and type checked. When you contribute code to NAVFITX, the github CI/CD will run linting, formatting, and type checking checks against pushed code. Pull requests that do not pass these check will not be merged.

To run these checks against your code locally before pushing, you must install the pre-commit hooks defined in the [.pre-commit-config.yaml](https://github.com/tristan-white/navfitx/blob/main/.pre-commit-config.yaml) file by running this command from the root of the clone repo:

```
uv run pre-commit install
```

Now any time you commit your code, the pre-commit hooks will run and preform linting, formatting, and type checks on your code.

<!-- ## Reading Microsoft Access Database Files in Linux

Access Database files (.accdb) can be read by installing MDBTools:

`sudo apt install mdbtools` -->

<!-- > NOTE for Linux:
> f you see the error `This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.`, do a `sudo apt install libxcb-cursor0`, then run again.
> If you see the error `ImportError: libodbc.so.2: cannot open shared object file: No such file or directory`, install unixodbc: `sudo apt install unixodbc`. -->
