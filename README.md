# parsedump
Disclaimer: I am not a trained devloper. I'm learning to program as I write little scripts that are useful to me. This script was written for my own use, and is neither warranted nor supported by my employer.

Parsedump processes credential dump files of various input formats and outputs them in a delimited format that is easier to process or ingest into other systems.

usage: parsedump.py [-h] -t TYPE [-d DELIMITER] [-q QUALIFIER] [-o OUTFILE] FILE

Parsedump supports the following input formats:

Pony http_list - format: protocol://username:password@site

Keybase - format: PCName[space]Site[space]Username[space]Password

Output is in the format:
	[qualifier]username[qualifier][delimeter][qualifier]password[qualifier]
