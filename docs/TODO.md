A tentative list of upcoming features (:bulb:) and implementation changes (:wrench:).

- [ ] :bulb: Support binary distributions that don't require the user to have Python installed.
- [ ] :bulb: Make distribution and installation instructions more intuitive.
- [ ] :bulb: Include update script in distribution. Remember to properly handle possibly existing `config.yaml`s.
- [ ] :bulb: Stop exposing `ConfigError`s and `CommandError`s and define more graceful output.
- [x] :bulb: Allow whitespace in -c/--channel option for more flexible searches (necessary if user is in multiple servers with the same dedicated channel, like "waifu-spam".
- [ ] :wrench: Figure out a better alternative to the the ENTER listener when prompting confirmation since this leaves an awkward newline at script termination.
- [ ] :wrench: Clean up the `parse_args` process and make better use of `argparse`'s error handling functionality, or migrate to other CLI libraries altogether.
- [ ] :wrench: ~~Enhance [build.ps1](build/build.ps1) to clean up even upon error, such as removing the generated `*.egg-info` directories.~~ Also maybe make it report how long the build takes since they take quite a while lol.
- [ ] :wrench: Maybe use environment variables instead of [meta.json](build/meta.json) to maintain version string since using [update.py](build/update.py) to modify 3 places at once seems like a massive code smell.
- ~~:wrench: Maybe migrate from [PyYAML](https://pyyaml.org/) to [ruamel.yaml](https://pypi.org/project/ruamel.yaml/).~~
- ~~:wrench: Use [rich logging](https://rich.readthedocs.io/en/stable/logging.html) instead of `rich.print` to fix the pervasive `if verbose:` lines.~~
- [x] :wrench: Make and maintain a fresh virtual environment to test builds in so it's possible to spot dependency errors (and because this might be how users actually try them).
