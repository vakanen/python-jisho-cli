# python-jisho-cli
A simple Python 3 script for searching the [Jisho dictionary](https://jisho.org/) using its public API.

<details>
  <summary>CLI example</summary>

![CLI example](example.svg?raw=true)
</details>

## Package dependencies

- [appdirs](https://pypi.org/project/appdirs/)
- [Requests](https://pypi.org/project/requests/)
- [PyYAML](https://pypi.org/project/PyYAML/)
- [termcolor](https://pypi.org/project/termcolor/)

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
