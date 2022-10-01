# Change Log

## Before I Knew What I Was Doing

![0.0.1](https://img.shields.io/badge/version-0.0.1-brightgreen)

- Initial distribution.

![0.0.2](https://img.shields.io/badge/version-0.0.2-brightgreen)

- Make the pause hotkey CAPSLOCK have effect during the [revert-window](#configuration-reference) delay as well (originally only the abort key ESC had effect).
- Add new configuration preference [keep-failsafe](#configuration-reference).

![0.0.3](https://img.shields.io/badge/version-0.0.3-brightgreen)

- Raise `ConfigFileError` with a helpful message if the configuration file is not valid YAML.
- Fix [requirements.txt](requirements.txt) to not include the installed waifu-roller dist since it points to a path on my local machine.
- Now stores configuration file template as a YAML file instead of as a `str` constant.
- Enhance development tool [build.ps1](build/build.ps1) to improve handling of requirements.txt and verifying installation of the correct .whl build.

![0.0.4](https://img.shields.io/badge/version-0.0.4-brightgreen)

- Unpausing the program with CAPSLOCK now focuses the Discord window if it wasn't already active.
- Losing focus on the Discord window while rolling now suspends rolling until it is the active window again.
- After the program is loaded, it displays a tip for CAPSLOCK pausing in addition to ESC aborting now.
- Now using relative imports (I didn't understand packages).

![0.0.5](https://img.shields.io/badge/version-0.0.5-brightgreen)

- Whitespace is now allowed for the -c/--channel argument and default channel configuration. This is useful for distinguishing similarly named channels in different servers, like "bot-spam server1" and "bot-spam server2".

![0.0.6](https://img.shields.io/badge/version-0.0.6-brightgreen)

- Add skip-confirmation [configuration option](REFERENCE.md#configuration-reference).

## After I <u>Kind of</u> Know What I'm Doing

![0.1.0](https://img.shields.io/badge/version-0.1.0-brightgreen)

- Revamp development environment by properly configuring the setup files and writing a few independent [scripts](../scripts/).
- Make the package read the configuration file template from a Python module instead of a YAML file because it wasn't getting packaged with setup.py. This is also before I found out about [packaging data files](https://setuptools.pypa.io/en/latest/userguide/datafiles.html).
