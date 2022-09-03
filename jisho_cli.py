#!/usr/bin/env python3

"""This is a Python 3 script for dictionary lookups from the Jisho.org
   online Japanese language dictionary, using its public API.

   This script is not affiliated with Jisho.org.
   The license text below applies to this script file, and is not related to
   Jisho.org or its language data sources' licensing in any way.

   For more information about Jisho and the language data sources it uses,
   please see the Jisho.org website:
   https://jisho.org/about
"""

# This script copyright 2021 https://github.com/vakanen
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse
import os

import appdirs
import requests
import yaml
from colorama import init
from termcolor import colored, cprint

SCRIPT_VERSION = '0.2.4'
SCRIPT_NAME = 'jisho_cli'

CFG_PATH = os.path.join(appdirs.user_config_dir(SCRIPT_NAME), 'config.yml')

# Try to open user-defined preferences
try:
    with open(file=CFG_PATH, mode='r', encoding='utf-8') as f_cfg:
        CFG = yaml.safe_load(f_cfg)
# But fall back to defaults if user config didn't exist.
# Hardcoding this instead of reading the repo config, because
# the user could've installed this package using custom tools
# where we don't know the location (or even the existence) of config.yml.
except FileNotFoundError:
    CFG = yaml.safe_load("""
        # The Jisho API url to use for lookups
        # Default value: https://jisho.org/api/v1
        api_base_url: https://jisho.org/api/v1

        # How many dictionary definitions to return, at most.
        # Use zero for no limit.
        # Value has to be zero or a positive integer.
        # Default value: 3
        max_results_default: 3

        # For possible values, see: https://pypi.org/project/termcolor/
        warning_text_color: yellow # Default value: yellow
        success_text_color: green # Default value: green

        # By default, the script makes sure its name matches
        # this config file's path, for naming consistency
        # (eg: "~/.config/jisho-cli/config.yml").
        # You can ignore this check by changing this value to True.
        # Default value: False
        ignore_script_name_mismatch: False
    """)
assert CFG is not None

# Initialize Colorama for platform independent terminal colour support.
init()


def print_warning(msg):
    """Print helper for colored output.
    """
    cprint(msg, CFG['warning_text_color'])


if not CFG['ignore_script_name_mismatch']:
    this_script_name = os.path.splitext(os.path.basename(__file__))[0]
    if SCRIPT_NAME != this_script_name:
        print_warning(f'This script name "{this_script_name}" != '
                      '{SCRIPT_NAME}".')
        print_warning('(You can turn off this warning in the config '
                      'file with the ignore_script_name_mismatch option.)\n')


def lookup(phrase):
    """Perform API lookup with a string.
    Prints a warning on non-HTTP 200 response (if it didn't except).
    Returns a JSON object.
    """
    url = CFG['api_base_url'] + '/search/words?keyword=' + phrase
    resp = requests.get(url, timeout=10.0)
    resp.raise_for_status()
    expected_response = 200
    if resp.status_code != expected_response:
        print_warning(f'Warning: Unexpected HTTP response {resp.status_code} '
                      f'(expected {expected_response})')
    json_obj = resp.json()
    api_response_status = json_obj['meta']['status']
    if api_response_status != expected_response:
        print_warning('Warning: Unexpected API status code '
                      f'{api_response_status} (expected {expected_response})')
    if api_response_status != resp.status_code:
        print_warning(f'Warning: API status code ({api_response_status}) '
                      f'differs from HTTP response ({resp.status_code})')
    return json_obj


def main():
    """Entry point"""
    def maxres_type(number):
        """Int type for argparse that requires values >= 0"""
        number = int(number)
        if number < 0:
            raise argparse.ArgumentTypeError('Needs to be an integer >= 0')
        return number

    def phrase_type(phrase):
        """Str type for argparse that requires values with len > 0"""
        if len(phrase) == 0:
            raise argparse.ArgumentTypeError('Phrase cannot be empty')
        return phrase

    parser = argparse.ArgumentParser(
        prog=SCRIPT_NAME,
        description='Script for searching the Jisho.org dictionary from the '
                    'CLI.')
    parser.add_argument('phrase',
                        metavar='<one or more search keyword(s)>',
                        type=phrase_type,
                        help='Word(s) to perform a Jisho.org dictionary API '
                             'lookup with. Can be in English or Japanese '
                             '(rōmaji input is also supported).')
    parser.add_argument('-m', '--max-results',
                        metavar='N', type=maxres_type,
                        default=CFG['max_results_default'],
                        help='Limit the maximum amount of results shown.')
    parser.add_argument('--version', action='version',
                        version='%(prog)s version ' + SCRIPT_VERSION,
                        help='Show version number.')
    args = parser.parse_args()

    json_data = lookup(args.phrase)

    num_results = len(json_data['data'])
    if num_results == 0:
        print(f'No results for {colored(args.phrase, attrs=["bold"])}')
        return

    def print_result_main(num, res):
        print(f'{num} result(s) for {colored(res, attrs=["bold"])}.')

    def print_definition(word, reading, num_forms):
        output = '\n' +\
            colored('Definition'
                    if num_forms == 0
                    else '\tAlt. form', CFG['success_text_color']) + ': '
        if word is not None:
            output += word
        elif reading is not None:
            output += reading
        if word is not None and reading is not None and reading != word:
            output += ' (' + reading + ')'
        if num_forms != 0:
            output += ' (' + str(num_forms + 1) + ')'
        print(output)

    print_result_main(num_results, args.phrase)
    if 0 < args.max_results < num_results:
        print(f'Limiting output to {args.max_results} result(s) as per '
              '-m/--max-results.')

    def enumerate_definitions(json_data, start=1):
        for i, definition in enumerate(json_data["data"], start):
            if i > args.max_results > 0:
                break
            for form_num, japanese in enumerate(definition['japanese']):
                reading = japanese.get('reading')
                word = japanese.get('word')
                print_definition(word, reading, form_num)
                # Alt. form; don't output same definitions again
                if form_num != 0:
                    continue
                for _, sense in enumerate(definition['senses'], start=1):
                    pos = ', '.join(sense['parts_of_speech'])
                    print(f'\t({pos}):')
                    for j, english in enumerate(sense['english_definitions'],
                                                start=1):
                        print(f'\t\t{j}: {english}')

    enumerate_definitions(json_data)
    print()


if __name__ == '__main__':
    main()
