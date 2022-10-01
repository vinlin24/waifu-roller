<!-- https://github.com/marketplace/actions/dynamic-badges -->
![Build Version](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/vinlin24/b4b5eb0dba19ef0cadea7eb95bd0d252/raw/badge.json)
![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)

# Coder's Waifu Roller

## Description

**Command line tool for rolling anime/game characters with the Discord bot [Mudae](https://top.gg/bot/432610292342587392).**

Suppose you're in the zone coding, but it's a new hour and you can roll for waifus again. Before you'd switch to Discord, find the channel, and brainlessly spam enter `$wa` or something. Now you can start the whole rolling sequence right from the command line:
```
waifu wa -c waifu-spam -n 10 -d
```

:mega: **No asking for user tokens, no Discord self-botting, no automatic claiming or sniping.** This project uses [PyAutoGUI](https://pypi.org/project/PyAutoGUI/) to automate the process of switching to the app, navigating to the channel, and entering commands. This silly script is intended to just free up your hands a little while you watch the rolls go by.

## Installation

### From Zip File (Windows)

**:information_source: Only supports v0.0.6 onwards.**

Download the desired zip file `waifu_roller-x.y.z.zip` from the [`exes`](dist/exes/) folder and extract it. At the moment, I have not finished implementing the installation process that adds the executable to PATH, so with this method, you will need to provide the full path to the `waifu.exe` within to use the CLI.

### With Python 3.10+

**:information_source: Only supports up to v0.0.6.**

Download the desired wheel file `waifu_roller-x.y.z-py3-none-any.whl` from the [`whls`](dist/whls/) folder and install it with pip:
```
pip install path/to/waifu_roller-x.y.z-py3-none-any.whl
```
You can verify that it's installed by running:
```
pip show waifu-roller
```

## Usage

The CLI command is `waifu`:
```
waifu wa -c waifu-spam -n 10 -d
```
This example rolls the Mudae command $wa 10 times in the channel named waifu-spam. The optional -d flag appends the daily commands $dk and $daily after the rolling session.

You can also omit arguments and opt to use the default values set in the [config.yaml](docs/REFERENCE.md#configuration) file. This could be useful if you roll most commonly in a specific channel on a specific server:
```
waifu
```

This program supports [hotkeys](docs/REFERENCE.md#hotkeys) to assist your *competitive waifu snatching*. You can pause and resume rolling with CAPSLOCK to claim a character/kakera/whatnot, or abort altogether with ESC.

As usual, use the help flag for a full list of arguments, or use the config flag to get the full path to your [configuration file](docs/REFERENCE.md#configuration):
```
waifu --help
waifu --config
```

## References and Configuration

See [REFERENCE.md](docs/REFERENCE.md).

## Development

As of now, the builds have only been tested on my local PC, which is a Windows 11 64-bit system.

If you want to simulate my development environment:

<table>
<tr>
    <th>Windows</th>
    <th>POSIX</th>
</tr>
<tr>
<td>

```console
git clone "https://github.com/vinlin24/waifu-roller.git"
cd waifu-roller
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e .
```

</td>
<td>

```console
git clone "https://github.com/vinlin24/waifu-roller.git"
cd waifu-roller
python3 -m venv .venv
source .venv/bin/activate
pip3 install -e .
```

</td>
</tr>
</table>


See [TODO.md](docs/TODO.md).

See [CHANGELOG.md](docs/CHANGELOG.md).
