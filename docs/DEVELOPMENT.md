# Development Instructions

As of now, the builds have only been tested on my local PC, which is a Windows 11 64-bit system.

If you want to simulate my development environment:

<table>
<tr>
    <th>Windows PowerShell</th>
    <th>Unix SH</th>
</tr>
<tr>
<td>

```powershell
git clone "https://github.com/vinlin24/waifu-roller.git"
cd "waifu-roller"
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements_dev.txt
pip install -e .
```

</td>
<td>

```console
git clone "https://github.com/vinlin24/waifu-roller.git"
cd "waifu-roller"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements_dev.txt
pip install -e .
```

</td>
</tr>
</table>

To update the semantic version, edit the `metadata.version` value in [setup.cfg](setup.cfg). Then run:


```console
python scripts/sync_version.py
```

This will sync the version string to relevant parts of the project, like `__version__` in [`__init__.py`](src/waifu/__init__.py).

To build the project source into a distributable wheel file:

```console
powershell.exe -NoProfile -File scripts/build.ps1
```

To install a fresh version of the latest distribution in your global `site-packages`, you can run:

```console
python scripts/install.py
```

This will take the last whl file in [`dist`](dist) and install it using the interpreter in your global environment. It also wipes your `config.yaml` file, if exists. This can help better simulate a completely fresh start as opposed to working with the version installed in the virtual environment with `pip install -e .`.