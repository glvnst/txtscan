#!/usr/bin/python
""" Report on the content of a text file, specifically the non-alpha parts """
import re
import collections
import argparse

NONPRINTING_REGEX = re.compile((r'[^A-Za-z0-9\ \r\n\,\<\.\>'
                                r'\/\?\!\@\#\$\%\^\&\*\(\)\-\_\=\+'
                                r'\[\]\{\}\;\:\'\"\|\\]'))
LINEENDING_REGEX = re.compile(r'[\r\n]+$')
ENDING_TYPEMAP = {'\r\n': r'\r\n  (Windows)',
                  '\n': r'\n (UNIX / OS X)',
                  '\r': r'\r (OS 9, Older)'}

VerboseChar = collections.namedtuple("VerboseChar", ['ord', 'char'])
VerboseChar.__repr__ = lambda self: '{0.char!r} (chr {0.ord})'.format(self)


def nonprinting_characters(string):
    """ Report on the content of the string """
    return [(match.start(), VerboseChar(ord(match.group(0)), match.group(0)))
            for match
            in NONPRINTING_REGEX.finditer(string)]


def get_ending(string):
    """ Return the line ending characters at the end of the line """
    match = LINEENDING_REGEX.search(string)
    if match:
        return match.group(0)
    return ''


def print_reports(report_list):
    """ Print the dictionary reports in the specified list """
    for report_name, report_dict, formatter in report_list:
        if report_dict:
            print "  {}:".format(report_name)
            for item, item_count in report_dict.items():
                suffix = "time" if item_count == 1 else "times"
                print "    {}: {:,} {}".format(formatter(item), item_count,
                                               suffix)
        else:
            print "  No {}.".format(report_name)


def main():
    """ The primary function called for command-line execution """
    argp = argparse.ArgumentParser(description=(
        "Print information about the characters in the input text"))
    argp.add_argument('input', nargs='+', type=argparse.FileType('r'), help=(
        "The file(s) to scan. Use '-' for standard input."))
    argp.add_argument('-v', '--verbose', action="store_true", help=(
        "Verbosely report on each interesting character on each line"))
    args = argp.parse_args()

    verbose = args.verbose

    for input_file in args.input:
        byte_count = 0
        line_count = 0
        endings_summary = collections.defaultdict(int)
        char_summary = collections.defaultdict(int)

        print input_file.name
        for (line_number, line) in enumerate(input_file):
            byte_count += len(line)
            line_count += 1
            endings_summary[get_ending(line)] += 1

            for pos, char in nonprinting_characters(line):
                char_summary[char] += 1
                if verbose:
                    print "  L{} C{}: {!r}".format(line_number, pos, char)

        print "  Bytes: {:,}".format(byte_count)
        print "  Lines: {:,}".format(line_count)
        # The format is: ["Report Name", report_dict, item_formatter_function]
        print_reports([
            ['Interesting Characters', char_summary, str],
            ['Line Endings', endings_summary,
             lambda x: ENDING_TYPEMAP.get(x, repr(x))]
        ])


if __name__ == '__main__':
    main()
