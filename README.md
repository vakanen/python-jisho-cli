# python-jisho-cli
A simple Python 3 script for searching the [Jisho.org](https://jisho.org/) Japanese language dictionary API from the terminal.

<details>
  <summary>CLI example (click to show)</summary>

![CLI example](example.svg?raw=true)
</details>

## Package dependencies

- [appdirs](https://pypi.org/project/appdirs/)
- [Requests](https://pypi.org/project/requests/)
- [PyYAML](https://pypi.org/project/PyYAML/)
- [termcolor](https://pypi.org/project/termcolor/)

## Usage

`jisho_cli.py` `[-h] [-m N] [--version]` `<one or more search keywords>`

Examples:
- `./jisho_cli.py Test`
- `./jisho_cli.py Test |less # Results piped to less`

### Config file location

#### Linux
`~/.config/jisho_cli/config.yml`

### Positional arguments
- <one or more search keyword(s)>

### Optional arguments
- `-h, --help` ― `show this help message and exit`
- `-m N, --max-results N` ― `Limit the maximum amount of results shown.`
- `--version` ― `Show version number and exit.`
