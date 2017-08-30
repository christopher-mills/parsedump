#!/usr/bin/python
import argparse, csv, sys, re, json, os, subprocess
from time import gmtime, strftime
parser = argparse.ArgumentParser()
parser.add_argument('filename', metavar='FILE', type=str,help='Specify a file name')
parser.add_argument('-t','--type',type=str,required=True,help='Specify the dump type (pony,keybase,phisher,phisher2,pinterest)')
parser.add_argument('-d','--delimiter',type=str,help='Specify a delimiter (default is pipe)')
parser.add_argument('-q','--qualifier',type=str,help='Specify a text qualifier to surround the fields (default is double quotes)')
parser.add_argument('-o','--outfile',type=str,help='Specify an output file, otherwise defaults to STDOUT')
parser.add_argument('-u','--upload',action='store_true',help='Upload data to MACE')
parser.add_argument('--breach-method',type=str,help='Specify a breach method')
parser.add_argument('-c','--cert',type=str,help='Specify the path to your MACE cert')
parser.add_argument('-s','--string',type=str,help='Specify the path to your MACE connection string')
parser.add_argument('-p','--path',type=str,help='Specify the path to the MACE uploader script')
parser.add_argument('--datapath',type=str,help='Specify the path to write data for MACE upload. Default is pwd')
args = parser.parse_args()
f = open(args.filename, 'r')
delimiter = '|'
qualifier = '"'
breachMethod = 'Unknown'
macePath = '~/mace/DataUploader.py'
if args.delimiter:
	delimiter = args.delimiter
if args.qualifier:
	qualifier = args.qualifier
if args.outfile:
	outfile = open(args.outfile,'w')
if args.breach_method:
	breachMethod = args.breach_method
if args.path:
	macePath = args.path
if args.cert:
	maceCert = args.cert
if args.string:
	maceConnectionString = args.string
if args.upload:
	datapath='.'
	if args.datapath:
		datapath=args.datapath
	if not os.path.exists(datapath):
		os.makedirs(datapath)
	if not os.path.exists(datapath + '/Data'):
		os.makedirs(datapath + '/Data')
	with open(datapath + '/BreachMetadata.json', 'w') as breachMetadataFile:
		json.dump({'AbuseVector': '', 'BotNetName': '', 'BreachActor': '', 'BreachCreationTime': strftime("%Y-%m-%dT%H:%M:%S +00:00", gmtime()),'BreachMethod': breachMethod,'BreachNotes': '','BreachSource': args.type,'BreachTarget': '','BreachTime': strftime("%Y-%m-%dT%H:%M:%S +00:00", gmtime()),'HashType': '','PartnerIdentifier': '','SecretFormat': 'Clear'},breachMetadataFile, sort_keys=True, indent=4)
	outfile = open(datapath + '/Data/BreachData.txt','w')

for line in f:
	if args.type == 'comma':
		# Comma format is: Email,Password
                if line.count(',') < 1:
                        continue
                user=line.split(',')[0].rstrip('\n')
                password=line.split(',')[1].rstrip('\n')
	if args.type == 'semi':
		# Semi format is: Email;Password
		if line.count(';') < 1:
			continue
		user=line.split(';')[0].rstrip('\n')
		password=line.split(';')[1].rstrip('\n')
        if args.type == 'colon':
                # Semi format is: Email;Password
                if line.count(':') < 1:
                        continue
                user=line.split(':')[0].rstrip('\n')
                password=line.split(':')[1].rstrip('\n')
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
	elif args.upload:
		dumpwriter = csv.writer(outfile,delimiter=delimiter,quotechar=qualifier,quoting=csv.QUOTE_MINIMAL)
	else:
		dumpwriter = csv.writer(sys.stdout,delimiter=delimiter,quotechar=qualifier,quoting=csv.QUOTE_MINIMAL)
	dumpwriter.writerow([user,password])
if args.upload:
	mace_command = [macePath, datapath, maceCert, maceConnectionString]
	mace_process = subprocess.Popen(mace_command)
