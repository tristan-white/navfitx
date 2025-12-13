> Note: NAVFITX is still in development. It may contain bugs, incomplete features, and/or breaking changes.

# NAVFITX

NAVFITX is a drop-in replacement for NAVFIT98A.

See [here](./docs/navfitx.pdf) for more information about why NAVFIT98 needs to be replaced.

| Feature | NAVFIT98 v33 | NAVFITX | 
|---------|---------------|---------|
| Export Reports as PDF | ✅ | ✅ |
| Runs on Windows | ✅ | ✅ |
| Runs on MacOS | ❌ | ✅ |
| Runs on Linux | ❌ | ✅ |
| Install & Use w/out Admin Privileges | ❌ | ✅ |
| What-You-See-Is-What-You-Get (WYSIWYG)<br>for text blocks | ❌ | ✅ | 
| Export data as sqlite database | ❌ | ✅ |

## Installation

The quickest way to use navfitx is to use uv:

1. [Install uv](https://docs.astral.sh/uv/getting-started/installation/):
2. Run `uvx navfitx gui`. NAVFITX is now running!

<!-- > NOTE for Linux:
> f you see the error `This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.`, do a `sudo apt install libxcb-cursor0`, then run again.
> If you see the error `ImportError: libodbc.so.2: cannot open shared object file: No such file or directory`, install unixodbc: `sudo apt install unixodbc`. -->

## Help NAVFITX Succeed

If you find a bug, have a question, or have feedback/a request for an enhancement, please create a [new issue](https://github.com/tristan-white/navfitx/issues) to track it.

I'd like to see NAVFITX replace NAFIT98A in the fleet. I'm looking for user testimonials from anyone that's used NAVFIT98A or eNavFit in order to answer the "why is this important" when I make the pitch to current NAVFIT98 stakeholders within the Navy. If you have feedback on these programs, please provide it here:

- [Provide feedback on NAVFIT98A](https://github.com/tristan-white/navfitx/discussions/1)
- [Provide feedback on eNavFit](https://github.com/tristan-white/navfitx/discussions/2) (if you had the chance to use it before it was shut down)