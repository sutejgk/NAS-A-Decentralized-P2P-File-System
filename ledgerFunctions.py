import json
from os import path
from random import randint

# macros
LEDGER_PATH = "ledger.json"

#
# Function to add a node to the ledger file
#
def add_node(ip, pubKey):

	# checks if ledger file exists
	if (path.exists(LEDGER_PATH) == False):
		return False

	# read the ledger file into a dictionary
	with open(LEDGER_PATH) as f:
		ledger = json.load(f)

	# new node variable
	node = {"IP" : ip, "Key" : pubKey}

	# add it to the ledger
	ledger["Nodes"].append(node)

	# Serializing json
	ledger_object = json.dumps(ledger, indent = 4)

	# Writing to sample.json
	with open(LEDGER_PATH, "w") as outfile:
		outfile.write(ledger_object)

#
# Function to add a node to the ledger file
#
def add_first_node(ip, pubKey):

	# read the ledger file into a dictionary
	ledger = {}

	# new node variable
	node = {"IP" : ip, "Key" : pubKey}

	# add it to the ledger
	ledger["Nodes"] = [node]

	# add en empty files list to the ledger
	ledger["Files"] = []

	# Serializing json
	ledger_object = json.dumps(ledger, indent = 4)

	# Writing to sample.json
	with open(LEDGER_PATH, "w") as outfile:
		outfile.write(ledger_object)


#
# Function to add a file to the ledger file
#
def add_file(filename, ownerIP):

	# checks if ledger file exists
	if (path.exists(LEDGER_PATH) == False):
		return False

	# read the ledger file into a dictionary
	with open(LEDGER_PATH) as f:
		ledger = json.load(f)

	# new node variable
	newfile = { "Filename" : filename, "Owner IP" : ownerIP, "Shards" : get_ips()}

	# check if client is the atual owner of the file
	for index, file in enumerate(ledger["Files"]):
		if file["Filename"] == filename:
			del ledger["Files"][index]
			

	# add it to the ledger
	ledger["Files"].append(newfile)

	# Serializing json
	ledger_object = json.dumps(ledger, indent = 4)

	# Writing to sample.json
	with open(LEDGER_PATH, "w") as outfile:
		outfile.write(ledger_object)

#
# Function that returns the shard fiename as stored on the server
#
def get_shard(filename, IP):

	# checks if ledger file exists
	if path.exists(LEDGER_PATH) == False:
		return False

	# read the ledger file into a dictionary
	with open(LEDGER_PATH) as f:
		ledger = json.load(f)

	# list to store the ips for a file
	ips = []

	# check if client is the atual owner of the file
	for file in ledger["Files"]:
		if file["Filename"] == filename:
			return filename + str(file["Shards"].index(IP))

#
# Function to check if the filename is owned by the IP
#
def check_owner(filename, IP):

	# checks if ledger file exists
	if path.exists(LEDGER_PATH) == False:
		return False

	# read the ledger file into a dictionary
	with open(LEDGER_PATH) as f:
		ledger = json.load(f)

	# check if client is the atual owner of the file
	for file in ledger["Files"]:
		if file["Filename"] == filename and file["Owner IP"] == IP:
			return True

	return False

#
# Function to return the public key of an IP
#
def get_pubkey(IP):

	# checks if ledger file exists
	if path.exists(LEDGER_PATH) == False:
		return False

	# read the ledger file into a dictionary
	with open(LEDGER_PATH) as f:
		ledger = json.load(f)

	# check if client is the atual owner of the file
	for node in ledger["Nodes"]:
		if node["IP"] == IP:
			return node["Key"]

	print("Key not found for IP")
	return None

#
# Returns all the ips that store a file
#
def get_ips_for_file(filename):

	# checks if ledger file exists
	if path.exists(LEDGER_PATH) == False:
		return False

	# read the ledger file into a dictionary
	with open(LEDGER_PATH) as f:
		ledger = json.load(f)

	# list to store the ips for a file
	ips = []

	# check if client is the atual owner of the file
	for file in ledger["Files"]:
		if file["Filename"] == filename:
			ips = file["Shards"]

	return ips

#
# Function that returns a list of files owned by a client
#
def get_files_for_owner(IP):

	# checks if ledger file exists
	if path.exists(LEDGER_PATH) == False:
		return False

	# read the ledger file into a dictionary
	with open(LEDGER_PATH) as f:
		ledger = json.load(f)

	# list to store the filenames
	files = []

	# check if client is the atual owner of the file
	for file in ledger["Files"]:
		if file["Owner IP"] == IP:
			files.append(file["Filename"])

	return files

#
# Function to get the list of ips from the ledger
#
def get_ips():

	# checks if ledger file exists
	if (path.exists(LEDGER_PATH) == False):
		return False

	# read the ledger file into a dictionary
	with open(LEDGER_PATH) as f:
		ledger = json.load(f)

	# a list of just the ips
	ips = []

	# going through the data and getting all the ips
	for node in ledger["Nodes"]:
		ips.append(node["IP"])

	# returns the new list of ips
	return ips
