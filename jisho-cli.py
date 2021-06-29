#!/usr/bin/env python3

# -----------------------------------------------------------------------------
# This is a Python 3 script for dictionary lookups from the Jisho.org
# online Japanese language dictionary, using its public API.
#
# This script is not affiliated with Jisho.org.
# The license text below applies to this script file, and is not related to
# Jisho.org or its language data sources' licensing in any way.
#
# For more information about Jisho and the language data sources it uses,
# please see the Jisho.org website:
# https://jisho.org/about
# -----------------------------------------------------------------------------

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

import appdirs  # https://pypi.org/project/appdirs/
import argparse
import json
import os
import requests  # https://pypi.org/project/requests/
import sys
import yaml  # https://pypi.org/project/PyYAML/
from termcolor import colored, cprint  # https://pypi.org/project/termcolor/

SCRIPT_VERSION = '0.1'
SCRIPT_NAME = 'jisho-cli'

CFG_PATH = os.path.join(appdirs.user_config_dir(SCRIPT_NAME), 'config.yml')
CFG = yaml.safe_load(open(CFG_PATH))


def print_warning(msg):
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
    r = requests.get(url)
    expected_response = 200
    if r.status_code != expected_response:
        print_warning(f'Warning: Unexpected HTTP response {r.status_code} '
                      '(expected {expected_response})')
    j = r.json()
    api_response_status = j['meta']['status']
    if api_response_status != expected_response:
        print_warning(f'Warning: Unexpected API status code '
                      '{api_response_status} (expected {expected_response})')
    if api_response_status != r.status_code:
        print_warning(f'Warning: API status code ({api_response_status}) '
                      'differs from HTTP response ({r.status_code})')
    return j


def main():
    """Entry point"""
    def maxres_type(n):
        """Int type for argparse that requires values >= 0"""
        n = int(n)
        if n < 0:
            raise argparse.ArgumentTypeError('Needs to be an integer >= 0')
        return n

    parser = argparse.ArgumentParser(
        prog=SCRIPT_NAME,
        description='Script for searching the Jisho.org dictionary from the '
                    'CLI.')
    parser.add_argument('phrase',
                        metavar='<one or more search keyword(s)>',
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

    # Get the JSON
    j = lookup(args.phrase)

    num_results = len(j['data'])
    if num_results == 0:
        print('No results for {}'.format(colored(args.phrase, attrs=['bold'])))
        return

    def print_result_main(num, x):
        print('{} result(s) for {}.'.format(num, colored(x, attrs=['bold'])))

    def print_definition(num, word, reading, num_forms):
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
    for i, definition in enumerate(j["data"], start=1):
        if i > args.max_results > 0:
            break
        for form_num, japanese in enumerate(definition['japanese']):
            reading = japanese.get('reading')
            word = japanese.get('word')
            print_definition(i, word, reading, form_num)
            if form_num != 0:  # Alt. form; don't output same definitions again
                continue
            for i, sense in enumerate(definition['senses'], start=1):
                pos = ', '.join(sense['parts_of_speech'])
                print(f'\t({pos}):')
                for i, english in enumerate(sense['english_definitions'],
                                            start=1):
                    print(f'\t\t{i}: {english}')
    print('')


if __name__ == '__main__':
    main()
