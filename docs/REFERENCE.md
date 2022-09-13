## Command Reference

| Argument             | Type           | Description                                                                                                                                                                                                                                                                      | Example      |
| -------------------- | -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------ |
| command              | positional     | Name of the Mudae command to use to roll for characters. It should be unprefixed (no $, /, etc.).                                                                                                                                                                                | 'wa'         |
| -c/--channel CHANNEL | option (1 arg) | Query string to submit to the Discord quick switcher to locate the channel to roll in. You should try entering this query yourself first with Ctrl+K to make sure it brings up the expected channel. The program has no way of knowing if the correct channel has entered focus. | 'waifu-spam' |
| -n/--num NUM         | option (1 arg) | Number of times to roll in this session. Should be nonnegative. You can troll and put a massive number, but it's not our fault if you get banned for spam.                                                                                                                       | 10           |
| -d/--daily           | option (flag)  | Flag specifying whether the daily Mudae commands, $daily and $dailykakera, should be run in addition to the rolling this session.                                                                                                                                                |              |


You can also use the following flags to display helpful information instead of rolling:

| Flag         | Description                                          |
| ------------ | ---------------------------------------------------- |
| -h/--help    | Display help message and ignore all other arguments. |
| -v/--version | Display version of installed script.                 |
| --config     | Display path of configuration file.                  |

## Hotkeys

This program uses the [keyboard](https://github.com/boppreh/keyboard) module to implement hotkeys for convenience. At the moment, they aren't configurable and most likely won't be because it wouldn't make much sense to have character or control keys interfere with PyAutoGUI's key-sending.

| Hotkey   | Description                                                                                                                                                                                                                        |
| -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ESC      | Abort script by sending SIGINT to the program. Also handy to use if the [revert-window](#configuration-reference) preference is set, which gives a short window of delay if you choose to stay on Discord to react to a roll, etc. |
| CAPSLOCK | Pause/resume rolling. This is useful if you want to stop to claim a spawned character or kakera drop in the middle of a rolling session.                                                                                           |
## Configuration

:mega: **Your configuration file is here: `~/.config/waifu-roller/config.yaml`**

On first run, the script will try to initialize a configuration file for you at the above path. Default values and helpful comments are provided in the document, but you can refer to the reference below for detailed descriptions.

## Configuration Reference

| Field                   | Type    | Description                                                                                                                                                                                                  | Default      |
| ----------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------ |
| verbose                 | boolean | Program verbosity level, and include config file path tip on --help and command error.                                                                                                                       | true         |
| revert-window           | boolean | Whether to return to the window from which script was called after rolling is completed. Waits for a short delay first. In case you want to stay on Discord, ESC aborting and TAB pausing still have effect. | false        |
| keep-failsafe           | boolean | Whether to keep PyAutoGUI's fail-safe mechanism, where moving your mouse to a corner of the screen terminates the program.                                                                                   | true         |  |
| skip-confirmation       | boolean | Whether to skip the confirmation text after running the command.                                                                                                                                             | false        |
| defaults                | mapping | Values to use when command line arguments are omitted.                                                                                                                                                       |              |
| defaults.mudae-command  | string  | Default value for the command positional arg.                                                                                                                                                                | null (unset) |
| defaults.target-channel | string  | Default value for the -c/--channel option.                                                                                                                                                                   | null (unset) |
| defaults.num-rolls      | int     | Default value for the -n/--num option.                                                                                                                                                                       | null (unset) |