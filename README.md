[![MIT](https://img.shields.io/github/license/vakanen/python-jisho-cli)](LICENSE)
[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)

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
- [appdirs](https://pypi.org/project/appdirs/)
- [Requests](https://pypi.org/project/requests/)
- [PyYAML](https://pypi.org/project/PyYAML/)
- [termcolor](https://pypi.org/project/termcolor/)

### Installation example
```bash
git clone https://github.com/vakanen/python-jisho-cli
cd python-jisho-cli

# Move the config file
mkdir -p ~/.config/jisho_cli && cp ./config.yml "$_"

# Make the script executable
chmod +x ./jisho_cli.py

# Install requirements
pip install --user appdirs PyYAML requests termcolor

# Run the script
./jisho_cli.py "Test phrase" # Quotations for multi-words queries
./jisho_cli.py Test |less # Results piped to less
```

Optionally, to shorten the command:
```bash
# Alias in .bashrc or similar
alias jisho_cli=/path/to/python-jisho-cli/jisho_cli.py
```

### Config file location
#### Linux
`~/.config/jisho_cli/config.yml`
