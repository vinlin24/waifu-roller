A :wrench: indicates a change in implementation detail or workflow and does not have a visible effect on the distribution for this version.

![0.0.1](https://img.shields.io/badge/version-0.0.1-brightgreen)

- Initial distribution.

![0.0.2](https://img.shields.io/badge/version-0.0.2-brightgreen)

- Make the pause hotkey CAPSLOCK have effect during the [revert-window](#configuration-reference) delay as well (originally only the abort key ESC had effect).
- Add new configuration preference [keep-failsafe](#configuration-reference).

![0.0.3](https://img.shields.io/badge/version-0.0.3-brightgreen)

- Raise `ConfigFileError` with a helpful message if the configuration file is not valid YAML.
- (:wrench:) Fix [requirements.txt](requirements.txt) to not include the installed waifu-roller dist since it points to a path on my local machine.
- (:wrench:) Now stores configuration file template as a YAML file instead of as a `str` constant.
- (:wrench:) Enhance development tool [build.ps1](build/build.ps1) to improve handling of requirements.txt and verifying installation of the correct .whl build.

![0.0.4](https://img.shields.io/badge/version-0.0.4-brightgreen)

- Unpausing the program with CAPSLOCK now focuses the Discord window if it wasn't already active.
- Unfocusing the Discord window while rolling now suspends rolling until it is the active window again.
- After the program is loaded, it displays a tip for CAPSLOCK pausing in addition to ESC aborting now.
- (:wrench:) Now using relative imports (I didn't understand packages).

![0.0.5](https://img.shields.io/badge/version-0.0.5-brightgreen)

- Whitespace is now allowed for the -c/--channel argument and default channel configuration. This is useful for distinguishing similarly named channels in different servers, like "bot-spam server1" and "bot-spam server2".