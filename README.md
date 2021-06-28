# python-jisho-cli
A simple Python 3 script for searching the [Jisho dictionary](https://jisho.org/) using its public API.

![CLI example](example.svg?raw=true)

## Usage

`jisho-cli.py` `[-h] [-m N] [--version]` `<one or more search keywords>`

### Config file location

#### Linux
`~/.config/jisho-cli/config.yml`

### Positional arguments
  - <one or more search keyword(s)>

### Optional arguments
  - `-h, --help` ― `show this help message and exit`
  - `-m N, --max-results N` ― `Limit the maximum amount of results shown.`
  - `--version` ― `Show version number and exit.`
