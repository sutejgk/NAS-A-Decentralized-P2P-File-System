import os
import socket
import shutil
from textwrap import wrap

from ledgerFunctions import LEDGER_PATH

REQUEST_MAX_LENGTH = 128

#
# Pad a request string to REQUEST_MAX_LENGTH
# message => String
#
def pad_string(message):
	return message + ((REQUEST_MAX_LENGTH - len(message)) * ' ')

#
# Find the local IP address of a host
#
def find_ip():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	ip = str(s.getsockname()[0])
	s.close()
	return ip;


#
# Returns an array of split up byte strings into
# data => ByteString
# nodes => Int
# eg splitData("abcd", 2) = ["ac", "bd"]
#
def split_data_chunk_number(data, nodes): #splitData

	# declaring the output array
	outputArray = []

	# going over the number of nodes to create each string
	for num in range(nodes):

		# get the chunk size
		chunk = (len(data)/nodes) + 1

		# if that many bytes our not possible do till end
		if((num + 1) * chunk < len(data)):
			temp_string = data[int(num * chunk): int((num + 1) * chunk)]
		else:
			temp_string = data[int(num * chunk):]

		# appending to the array
		outputArray.append(temp_string)

	# array of length, nodes
	return outputArray

#
#   Return a list of equally sized data packets based on a fixed size
#
def split_data_chunk_size(data, chunk):

	# declaring the output array
	outputArray = []

	if len(data)%chunk == 0:
		nodes = int(len(data)/chunk)
	else:
		nodes = int(len(data)/chunk) + 1

	# going over the number of nodes to create each string
	for num in range(nodes):

		# if that many bytes our not possible do till end
		if((num + 1) * chunk < len(data)):
			temp_string = data[int(num * chunk): int((num + 1) * chunk)]
		else:
			temp_string = data[int(num * chunk):]

		# appending to the array
		outputArray.append(temp_string)

	# array of length, nodes
	return outputArray

#
# Returns a byte string from a split up array
# data_array => ByteString Array
# eg retrieveData(["ac", "bd"]) = "abcd"
#
def retrieveData(data_array):

	# declaring the output bytestring
	outputData = "".encode()

	# going though the array one by one
	for data in data_array:

		# append each part
		outputData += data

	# byte string with all the data
	return outputData

def clean_directory():
	# remove trailing files from previous network usage
	if os.path.isfile(LEDGER_PATH):
		os.remove(LEDGER_PATH)
	if os.path.isdir("directory"):
		shutil.rmtree("directory")
	if os.path.isdir("fico"):
		shutil.rmtree("fico")

	# add fresh directories for the new network to run on
	os.mkdir("directory")
	os.mkdir("fico")
