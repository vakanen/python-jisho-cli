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

import argparse
import os

import appdirs
import requests
import pykakasi
import yaml
from colorama import init
from termcolor import colored, cprint

SCRIPT_VERSION = '0.4.0'
SCRIPT_NAME = 'jisho_cli'

CFG_PATH = os.path.join(appdirs.user_config_dir(SCRIPT_NAME), 'config.yml')

# pylint: disable=too-many-locals

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


def main():
    # pylint: disable=too-many-branches, too-many-statements
    """Entry point"""
    def nonnegative_int(number):
        """Int type for argparse that requires values >= 0"""
        number = int(number)
        if number < 0:
            raise argparse.ArgumentTypeError('Needs to be constructible to an integer >= 0')
        return number

    def nonnegative_float(number):
        """Float type for argparse that requires values >= 0"""
        number = float(number)
        if number < 0:
            raise argparse.ArgumentTypeError('Needs to be constructible to a float >= 0')
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
                        nargs='+',
                        help='Word(s) to perform a Jisho.org dictionary API '
                             'lookup with. Can be in English or Japanese '
                             '(rōmaji input is also supported).')
    parser.add_argument('-m', '--max-results',
                        metavar='N', type=nonnegative_int,
                        default=CFG['max_results_default'],
                        help='Limit the maximum amount of results shown.')
    parser.add_argument('-d', '--decompound',
                        action='store_true',
                        help='Decompound the lexeme, using the first lookup result from the API '
                             'as base.')
    parser.add_argument('-D', '--decompound_literal',
                        action='store_true',
                        help='Same as --decompound, but use the "phrase" argument as-is, '
                             'character by character.')
    parser.add_argument('--timeout',
                        metavar='N', type=nonnegative_float, default=10.0,
                        help='Override for remote API connection timeout, in seconds. '
                             'If value equals zero, disables API timeout entirely.')
    parser.add_argument('--version', action='version',
                        version='%(prog)s version ' + SCRIPT_VERSION,
                        help='Show version number.')
    parser.set_defaults(decompound=False)
    parser.set_defaults(decompound_literal=False)
    args = parser.parse_args()

    # Because --decompound_literal implies --decompound
    if args.decompound_literal:
        args.decompound = True

    json_data = []

    def lookup(phrase):
        """Perform API lookup with a string.
        Prints a warning on non-HTTP 200 response (if it didn't except).
        Returns a JSON object.
        """
        url = CFG['api_base_url'] + '/search/words?keyword=' + phrase
        try:
            resp = requests.get(url, **{ 'timeout': None if args.timeout == 0 else args.timeout })
        except Exception as err:
            # --decompound is a special case where we might be doing several API lookups
            # in a row, so on timeout we suggest overriding that timeout limit.
            if args.decompound:
                # We're using a third party library for connections here, and the timeout
                # exception throws from yet another library that one is using. Doing a
                # "fuzzy" lookup here for an error message that seems like a timeout error,
                # so that we don't need to care about who throws the exception, or what its
                # actual name is.
                probably_timed_out = any(x in repr(err) for x in ('timeout', 'timed out'))
                if probably_timed_out:
                    raise RuntimeError("It seems the API connection timed out. You may wish "
                                       "to override the timeout limit with --timeout.") from err
            raise err
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

    def decompound(lexeme, recurse_depth = 0, converter = None):
        res = []
        if recurse_depth > 10:
            return res
        recurse_depth += 1
        if converter is None:
            converter = pykakasi.kakasi()
        stems = converter.convert(lexeme)
        for stem in stems:
            if len(lexeme) == 1:
                res.append(stem['orig'])
                continue
            if stem['orig'] == lexeme:
                for char in stem['orig']:
                    subcompound = converter.convert(char)
                    for substem in subcompound:
                        res += decompound(substem['orig'],
                                          recurse_depth=recurse_depth,
                                          converter=converter)
                break
            if stem['orig'] not in [v for k, v in stem.items() if k != 'orig']:
                res += decompound(stem['orig'],
                                  recurse_depth=recurse_depth,
                                  converter=converter)
            else:
                res += stem['orig']
        return res

    phrase = ' '.join(args.phrase)
    if args.decompound:
        stems = []
        if args.decompound_literal:
            stems += decompound(phrase)
        else:
            primary_result = lookup(phrase)
            if len(primary_result['data']) == 0:
                print(f'No results for {colored(phrase, attrs=["bold"])}')
            else:
                word = primary_result['data'][0]['japanese'][0].get('word', None)
                if word is None:
                    print('Could not find decompoundable results for '
                          f'{colored(phrase, attrs=["bold"])} (primary result was: '
                          f'"{primary_result["data"][0]["japanese"][0]}"). You may wish to '
                          'decompound it literally with -D/--decompound_literal, instead.')
                else:
                    print(decompound(word))
                    stems += decompound(word)
        if len(stems) > 0:
            print(f"Decompounding lexeme as stem(s): {stems}")
        for stem in stems:
            json_data.append(lookup(stem))
    else:
        json_data.append(lookup(phrase))

    def print_result_main(num, res):
        if not args.decompound:
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

    def enumerate_definitions(json_datum, start=1):
        for i, definition in enumerate(json_datum["data"], start):
            if args.decompound and i > start:
                break
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

    for json_datum in json_data:
        num_results = len(json_datum['data'])
        if num_results == 0:
            if not args.decompound:
                print(f'No results for {colored(phrase, attrs=["bold"])}')
                return
        print_result_main(num_results, phrase)
        if args.decompound:
            print('Decompounding lexeme from API primary search result as per -d/--decompound.')
        elif 0 < args.max_results < num_results:
            print(f'Limiting output to {args.max_results} result(s) as per '
                  '-m/--max-results.')
        enumerate_definitions(json_datum)
        print()


if __name__ == '__main__':
    main()
