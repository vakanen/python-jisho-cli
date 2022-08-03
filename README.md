[![MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Pylint](https://github.com/vakanen/python-jisho-cli/actions/workflows/pylint.yml/badge.svg)](https://github.com/vakanen/python-jisho-cli/actions/workflows/pylint.yml)

# python-jisho-cli
A simple Python 3 CLI for searching the [Jisho.org](https://jisho.org/) Japanese language dictionary directly from the terminal.

<details>
  <summary><i>Terminal example (click to show)</i></summary>

![Terminal example](example.svg?raw=true)
</details>

## Usage

`jisho-cli` `[-h] [-m N] [--version]` `<one or more search keywords>`

### Positional arguments
- <one or more search keyword(s)>

### Optional arguments
- `-h, --help` ― `show this help message and exit`
- `-m N, --max-results N` ― `Limit the maximum amount of results shown.`
- `--version` ― `Show version number and exit.`

## Installation

One-liner install with [pipx](https://github.com/pypa/pipx):

```bash
pipx install git+https://github.com/vakanen/python-jisho-cli.git
```

Creating a config file (optional):

```bash
# Linux example

# Get the git files
git clone https://github.com/vakanen/python-jisho-cli
pushd "./python-jisho-cli/"

# Copy the config file
mkdir -p ~/.config/jisho_cli && cp ./config.yml "$_"

# Remove the git files
popd
rm -rf "./python-jisho-cli/"
```

### Config file location
#### Linux
`~/.config/jisho_cli/config.yml`
#### Windows
`%LOCALAPPDATA%\jisho_cli\jisho_cli\config.yml`
