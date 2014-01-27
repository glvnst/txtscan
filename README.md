# textscan

A small command-line program that reports on general statistics and interesting characters inside a text file.

## Examples

	% textscan 1.eml /etc/moduli
	1.eml
	  Bytes: 97,910
	  Lines: 2,343
	  Interesting Characters:
	    '\t' (chr 9): 1 time
	  Line Endings:
	    \r\n  (Windows): 2,343 times
	/etc/moduli
	  Bytes: 242,153
	  Lines: 262
	  No Interesting Characters.
	  Line Endings:
	    \n (UNIX / OS X): 262 times

Standard input scanning works too:

	% date | textscan -
	<stdin>
	  Bytes: 29
	  Lines: 1
	  No Interesting Characters.
	  Line Endings:
	    \n (UNIX / OS X): 1 time

Verbose mode reports all the positions of the "interesting characters":

	% echo -e '\nwhat?\tin blazes\nis happening\r\nin\bthis\ttext' | textscan -v -
	<stdin>
	  L1 C5: '\t' (chr 9)
	  L3 C2: '\x08' (chr 8)
	  L3 C7: '\t' (chr 9)
	  Bytes: 44
	  Lines: 4
	  Interesting Characters:
	    '\x08' (chr 8): 1 time
	    '\t' (chr 9): 2 times
	  Line Endings:
	    \n (UNIX / OS X): 3 times
	    \r\n  (Windows): 1 time	

## What's "Interesting"?

Textscan only reports on **things that *aren't* in this list**:

- A-Z, a-z, 0-9
- space, newline (\n), carriage return (\r)
- comma, period, colon, semicolon, exclamation mark, question mark (',' and '.' and ':' and ';' and '!' and '?')
- greater than, less than ('<' and '>')
- forward slash, backslash ('/' and '\')
- these symbols: '@', '#', '$', '%', '^', '&', '*'
- the dash, underscore, equals, and plus symbols ('-', '_', '=', '+')
- open and close brackets and braces and parens: '[' and ']' and '{' and '}' and '(' and ')'
- single quotes and double quotes (' and ")
- pipe/vertical bar ('|')

** Note that both tab and the euro symbol are considered "interesting".**

## Help Message

	usage: textscan [-h] [-v] input [input ...]
	
	Print information about the characters in the input text
	
	positional arguments:
	  input          The file(s) to scan. Use '-' for standard input.
	
	optional arguments:
	  -h, --help     show this help message and exit
	  -v, --verbose  Verbosely report on each interesting character on each line

## To Do

- Although this is primarily aimed at scanning ASCII files, it would be nice (and probably not too hard) to add Unicode support, **particularly support for finding unicode errors**
- Add options to exclude certain characters from reporting or to scan only for certain characters
