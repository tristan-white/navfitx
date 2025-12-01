> Note: NAVFITX is still in development.

# NAVFITX

NAVFITX is a drop-in replacement for NAVFIT98A.

See [here](./docs/navfitx.pdf) for more information about why NAVFIT98 needs to be replaced.

| Feature | NAVFIT98A v33 | NAVFITX | 
|---------|---------------|---------|
| Export Reports as PDF | ✅ | ✅ |
| Runs on Windows 7 | ❌ | ❌ |
| Cross-Platform (Windows/MacOS/Linux) | ❌ | ✅ |
| Install & Use w/out Admin Privileges | ❌ | ✅ |
| Open Source | ❌ | ✅ |

## Installation

The simplest way to use navfitx is to open a terminal on your computer and copy and past two commands into it. On Windows, open powershell. On MacOS, open Terminal. (If you're on linux, you don't need help installing this.)

1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/):
    - Windows: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
    - MacOS or Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`
2. Close and reopen your terminal, then run: `uvx navfitx`. You're done!

> NOTE:
> If you see the error `This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.`, install `libxcb-cursor0`, then run again.
> If you see the error `ImportError: libodbc.so.2: cannot open shared object file: No such file or directory`, install unixodbc: `sudo apt install unixodbc`.

## Help NAVFITX Succeed

I'd like to see NAVFITX replace NAFIT98A in the fleet. I'm looking for user testimonials from anyone that's used NAVFIT98A or eNavFit in order to answer the "why is this important" when I make the pitch to current NAVFIT98 stakeholders within the Navy. If you have feedback on these programs, please provide it here:

- [Provide feedback on NAVFIT98A](https://github.com/tristan-white/navfitx/discussions/1)
- [Provide feedback on eNavFit](https://github.com/tristan-white/navfitx/discussions/2) (if you had the chance to use it before it was shut down)

Additionally, please consider giving this repo a ⭐ to help it gain visibility.

<!-- <a href='https://ko-fi.com/Q5Q41PEEPR' target='_blank'><img height='36' style='border:0px;height:36px;' src='https://storage.ko-fi.com/cdn/kofi5.png?v=6' border='0' alt='Buy Me a Coffee at ko-fi.com' /></a> -->