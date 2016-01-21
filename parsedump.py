#!/usr/bin/python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('filename', metavar='FILE', type=str,help='Specify a file name')
parser.add_argument('-t','--type',type=str,help='Specify the dump type (pony,keybase)')
parser.add_argument('-d','--delimiter',type=str,help='Specify a delimiter (default is comma)')
args = parser.parse_args()
f = open(args.filename, 'r')
if args.delimiter:
	delimiter = args.delimiter
else:
	delimiter = ','
for line in f:
	if args.type == 'pony':
		userPass=line.partition('//')[2].rpartition('@')[0]
		user=userPass.partition(':')[0]
		password=userPass.partition(':')[2]
		print user + delimiter + password
	if args.type == 'keybase':
		pcname=line.partition(' ')[0]
		password=line.rpartition(' ')[2]
		user=line.rpartition(' ')[0].rpartition(' ')[2]
		print user + delimiter + password,
