#!/usr/bin/python
import argparse, csv, sys, re
parser = argparse.ArgumentParser()
parser.add_argument('filename', metavar='FILE', type=str,help='Specify a file name')
parser.add_argument('-t','--type',type=str,required=True,help='Specify the dump type (pony,keybase,phisher,phisher2,pinterest)')
parser.add_argument('-d','--delimiter',type=str,help='Specify a delimiter (default is comma)')
parser.add_argument('-q','--qualifier',type=str,help='Specify a text qualifier to surround the fields (default is double quotes)')
parser.add_argument('-o','--outfile',type=str,help='Specify an output file, otherwise defaults to STDOUT')
args = parser.parse_args()
f = open(args.filename, 'r')
delimiter = ','
qualifier = '"'
if args.delimiter:
	delimiter = args.delimiter
if args.qualifier:
	qualifier = args.qualifier
if args.outfile:
	outfile = open(args.outfile,'w')
for line in f:
	if args.type == 'pony':
		# Pony format is: protocol://username:password@site
		userPass=line.partition('//')[2].rpartition('@')[0]
		user=userPass.partition(':')[0]
		password=userPass.partition(':')[2]
	if args.type == 'keybase':
		# Keybase format is: PCName[space]Site[space]Username[space]Password
		pcname=line.partition(' ')[0]
		password=line.rpartition(' ')[2].rstrip('\n')
		user=line.rpartition(' ')[0].rpartition(' ')[2]
	if args.type == 'phisher':
                # This format is: Time#username#:#IPAddr#UserAgent#Site
                if line.count('#') < 4:
                        continue
		linesplit=line.split('#')
		user=linesplit[1]
		password=linesplit[2]
		if len(user) < 1:
			continue
        if args.type == 'phisher2':
                # This format is: Username,Password#IPAddress#Hostname - UserAgent
                if line.count('#') < 2:
                        continue
                linesplit=line.split('#')
                userpass=linesplit[0]
		user=userpass.split(',')[0]
                password=userpass.split(',')[1]
        if args.type == 'phisher3':
                # This format is: Username,Password#IPAddress#Hostname - UserAgent
                if line.count('#') < 2:
                        continue
		notimestamp=line.split(' ')[1]
                linesplit=notimestamp.split('#')
                userpass=linesplit[0]
                user=userpass.split(',')[0]
	if args.type == 'pinterest':
		if "EMAIL->" in line:
			user=line.partition('->')[2].rstrip()
			password=f.next().rstrip()
		else:
			continue
	if args.type == 'zain':
		linesplit=line.split(",")
		user=linesplit[0]
		password=linesplit[1].rstrip()
		m = re.split(r'\d+$',user)
		user=m[0].rstrip()
		if user[0].isdigit():
			user=user[1:]
        if args.outfile:
        	dumpwriter = csv.writer(outfile,delimiter=delimiter,quotechar=qualifier,quoting=csv.QUOTE_MINIMAL)
	else:
		dumpwriter = csv.writer(sys.stdout,delimiter=delimiter,quotechar=qualifier,quoting=csv.QUOTE_MINIMAL)
       		dumpwriter.writerow([user,password])
