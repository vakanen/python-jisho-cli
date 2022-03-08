[![MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Pylint](https://github.com/vakanen/python-jisho-cli/actions/workflows/pylint.yml/badge.svg)](https://github.com/vakanen/python-jisho-cli/actions/workflows/pylint.yml)

# python-jisho-cli
A simple Python 3 CLI for searching the [Jisho.org](https://jisho.org/) Japanese language dictionary directly from the terminal.

<details>
  <summary><i>Terminal example (click to show)</i></summary>

![Terminal example](example.svg?raw=true)
</details>

## Usage

`jisho_cli.py` `[-h] [-m N] [--version]` `<one or more search keywords>`

### Positional arguments
- <one or more search keyword(s)>

### Optional arguments
- `-h, --help` ― `show this help message and exit`
- `-m N, --max-results N` ― `Limit the maximum amount of results shown.`
- `--version` ― `Show version number and exit.`

## Installation

### Package dependencies
Recommended to be installed via the *requirements.txt* file.

- [appdirs](https://pypi.org/project/appdirs/)
- [colorama](https://pypi.org/project/colorama/)
- [Requests](https://pypi.org/project/requests/)
- [PyYAML](https://pypi.org/project/PyYAML/)
- [termcolor](https://pypi.org/project/termcolor/)

### Installation example (Linux)
Optional: use a <a target="_blank" rel="noopener noreferrer" href="https://docs.python.org/3/library/venv.html">virtual environment</a>:

```bash
python -m venv venv
venv/scripts/activate
```

Installation:

```bash
git clone https://github.com/vakanen/python-jisho-cli
cd python-jisho-cli

# Move the config file
mkdir -p ~/.config/jisho_cli && cp ./config.yml "$_"

# Make the script executable
chmod +x ./jisho_cli.py

# Install requirements
pip install --user -r requirements.txt

# Run the script
./jisho_cli.py "Test phrase" # Quotations for multi-words queries
./jisho_cli.py Test |less # Results piped to less
```

Optionally, to shorten the invocation:

```bash
# Alias in .bashrc or similar
alias jisho_cli=/path/to/python-jisho-cli/jisho_cli.py
```

### Config file location
#### Linux
`~/.config/jisho_cli/config.yml`
#### Windows
`%LOCALAPPDATA%\jisho_cli\jisho_cli\config.yml`
