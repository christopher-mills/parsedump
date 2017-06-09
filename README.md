# parsedump
Disclaimer: I am not a trained devloper. I'm learning to program as I write little scripts that are useful to me. This script was written for my own use, and is neither warranted nor supported by my employer.

Parsedump processes credential dump files of various input formats and outputs them in a delimited format that is easier to process or ingest into other systems.

usage: parsedump.py [-h] -t TYPE [-d DELIMITER] [-q QUALIFIER] [-o OUTFILE]
                    [-u] [--breach-method BREACH_METHOD] [-c CERT] [-s STRING]
                    [-p PATH] [--datapath DATAPATH]
                    FILE

Parsedump supports the following input formats:

Pony http_list - format: protocol://username:password@site
Keybase - format: PCName[space]Site[space]Username[space]Password
Semi - format: username;password
phisher - format: Time#username#:#IPAddr#UserAgent#Site
phisher2 - format: Username,Password#IPAddress#Hostname - UserAgent
phisher3 - format: Username,Password#IPAddress#Hostname - UserAgent
pinterest - multiline format
zain - format: Username,Password (This dump contained extra characters that needed to be stripped out)

Output is in the format:
	[qualifier]username[qualifier][delimeter][qualifier]password[qualifier]

The MACE functionality adds options to generate metadata about the breach, as well as call an external script to upload the parsed data to a system for further processing.
-u enables this functionality
--breach-method captures the string for how the breach occured (phishing, db hack, etc)
-c is the path for the upload certificate
-s is the path for the connection string
-p is the path for the external uploader script
--datapath is the path to store the data used by the uploader script.
