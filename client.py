import socket
import sys
import os
import time
import helperFunctions as helper
import ledgerFunctions as ledger
import encryption

BYTES_TO_SEND = 1024
REQUEST_MAX_LENGTH = 128

#
# Creates a socket that has a connection with the specied host and port
#
def run_client(host, port=12345):

    #creates a new socket
    s = socket.socket()

    #connect the socket to the given host
    s.connect((host, port))

    #return the socket once created
    return s

#
# Lock all servers
#
def lock_servers():

    # logging
    print("Locking All Servers")

    # go through the ips and lock them
    for ip in ledger.get_ips():

        # get the key of the server we want to send to
        serverPubkey = ledger.get_pubkey(ip)

        # connect to the host you want to send file to
        s = run_client(ip)

        # create a push request for the server and encode it to bytes
        cmd = "lock " + helper.find_ip()

        # Encrypt cmd using servers public key
        encrypted_cmd = encryption.encrypt_using_public_key(cmd.encode(), serverPubkey)

        s.send(encrypted_cmd)

        # recieve response from server
        recv = s.recv(REQUEST_MAX_LENGTH).decode()

        # if error then stop
        if(recv.split()[0] == "Error"):

            # return false
            print(recv)
            return False

    # if everything goes smoothly
    return True



#
# Function to send out bytes of data from filename
#
def send_file(filename):

    # going to start locking all servers for a send file
    if(lock_servers() == False):
        return

    print("Began writing to all nodes in the network")
    print("******************************")
    print("******************************")

    # opening a file in binary
    f = open(filename, 'rb')

    # get rid of the path
    filename = filename.split("/")[-1]

    # getting all the data in a byte string
    byteString = f.read()

    # seperate it into files
    byteArray = helper.split_data_chunk_number(byteString, len(ledger.get_ips()))

    # get clients public key
    myPubkey = ledger.get_pubkey(helper.find_ip())

    # going through the list of ips and making the request
    for index, ip in enumerate(ledger.get_ips()):

        # get the key of the server we want to send the file to
        serverPubkey = ledger.get_pubkey(ip)

        # check if the ip is same as our ip
        if(ip == helper.find_ip()):

            # open a temporary file to store the received bytes
            try:
                file = open("directory/" + filename + str(index), 'wb')
            except:
                os.mkdir("directory")
                file = open("directory/" + filename + str(index), 'wb')

            # write to the file and exncrypt the data
            file.write(byteArray[index])

            # move forward in the for loop
            continue

        # connect to the host you want to send file to
        s = run_client(ip)

        print(filename)

        # create a push request for the server and encode it to bytes
        cmd = "push " + filename + str(index)

        # Encrypt cmd using servers public key
        encryptedCmd = encryption.encrypt_using_public_key(cmd.encode(), serverPubkey)

        s.send(encryptedCmd)

        # recieve response from server
        recv = s.recv(REQUEST_MAX_LENGTH).decode()

        # check if the servor responded with an error
        if(recv.split()[0] != "Error"):

            # get the string we want to send
            toSend = byteArray[index]
            byteCount = 0

            # logging
            print("Starting to send", len(toSend),"bytes to", ip)

            # get the range of things to send at a time
            for i in range(0, len(toSend), BYTES_TO_SEND):

                # if its too big then only till the end
                if(i + BYTES_TO_SEND >= len(toSend)):
                    byte = toSend[int(i):]
                else:
                    byte = toSend[int(i):int(i + BYTES_TO_SEND)]

                # encrypting whatever data we need to
                byte = encryption.encrypt_using_public_key(byte, myPubkey)

                # send the bytes
                s.send(byte)

                byteCount += BYTES_TO_SEND

                # print("Sent", byteCount, "bytes")

            # logging
            print("Finished sending file")
            print("******************************")

        # server did respond with error
        else:
            print("Something went wrong")

        s.close()

    # logging end of command
    print("******************************")

    # updating the ledger locally
    ledger.add_file(filename, helper.find_ip())

    # sending the update ledger command to everyone
    update_ledger()


#
# Receives a file
#
def receive_file(filename):

    # check if the client is the owner of the file
    if not ledger.check_owner(filename, helper.find_ip()):
        print("File not owned by this client")
        return

    # create the downloaded directory if it doesnt exist, and open a file to write in
    try:
        file = open("directory/" + filename, 'wb')
    except:
        os.mkdir("directory")
        file = open("directory/" + filename, 'wb')

    # going through the list of ips and making the request
    for index, ip in enumerate(ledger.get_ips_for_file(filename)):

        # get the key of the server we want to send the file to
        serverPubkey = ledger.get_pubkey(ip)

        print(helper.find_ip(), ip)
        # check if the current ip in the ledger is the clients
        if(ip == helper.find_ip()):

            # get the shard name for the file that is stored on the clients computer
            shard = ledger.get_shard(filename, ip)

            # open the shard to combine it with the rest of the file
            tempFile = open("directory/" + shard, 'rb')

            # copy the contents of the shard to the new file and decrypt the data
            file.write(tempFile.read())

            print("here")

            # continue iterating through the loop
            continue


        # connect to the host you want to receive files from
        s = run_client(ip)

        # gets the shard filename as stored on the host computer
        shard = ledger.get_shard(filename, ip)

        # create a pull request for the server and encode it to bytes
        cmd = helper.pad_string("pull " + shard)

        # Encrypt cmd using servers public key
        encryptedCmd = encryption.encrypt_using_public_key(cmd.encode(), serverPubkey)
        s.send(encryptedCmd)

        # recieve confirmation response from server
        receivedMessage = s.recv(REQUEST_MAX_LENGTH).decode()


        # check if the servor responded with an error
        if(receivedMessage.split()[0] != "Error"):

            print("Receiving shard from", ip)

            while True:


                #receive 1024 bytes at a time and decrypt the data
                bytes = s.recv(1024)
                bytes = encryption.decrypt_using_private_key(bytes)

                #write the decrypted data to a file
                file.write(bytes)


                #break infinite loop once all bytes are transferred
                if not bytes:
                    break

            # Server responded with an error
        else:
            print("Something went wrong while receiving the file.")


    # try to remove the original sharded message
    try:
        os.remove("directory/" + ledger.get_shard(filename, helper.find_ip()))
    except:
        print("Unable to remove shard from local directory")

    #close the file once transfer is complete
    file.close()


#
# Gets a copy of the current ledger from a known host, adds itself,
# and broadcasts to all servers
#
def pull_ledger(ip, serverPubkey):

    # connect to the ip
    s = run_client(ip)

    helper.clean_directory()

    # create a new node request for the server and encode it to bytes
    cmd = "pull_ledger ledger.json"

    # Encrypt cmd using servers public key
    encrypted_cmd = encryption.encrypt_using_public_key(cmd.encode(), serverPubkey)

    #Send the encrypted command to the server in bytes
    s.send(encrypted_cmd)

    # recieve confirmation response from server
    receivedMessage = s.recv(REQUEST_MAX_LENGTH).decode()
    print(receivedMessage)

    if(receivedMessage.split(' ', 1)[0] != "Error"):


        # generate a public and private key for the host computer
        pubkey = encryption.create_keys()

        #Encrypt the public key using server public key
        encrypted_pubkey = encryption.encrypt_using_public_key(pubkey.encode(), serverPubkey)

        #Encrypted public key is split into
        pubkey_split = []
        pubkey_split.append(encrypted_pubkey[0:REQUEST_MAX_LENGTH])
        pubkey_split.append(encrypted_pubkey[REQUEST_MAX_LENGTH:])
        print(pubkey)
        print(pubkey_split)


        for pubkey_part in pubkey_split:
            s.send(pubkey_part)

        print("Downloading ledger")
        #open a new ledger and store the received bytes
        file = open(ledger.LEDGER_PATH, 'wb')
        start = time.time()


        while True:

            #receive 1024 bytes at a time and write them to a file
            encrypted_bytes = s.recv(1024)
            bytes = encryption.decrypt_using_private_key(encrypted_bytes)
            file.write(bytes)

            #break infinite loop once all bytes are transferred
            if not bytes:
                break

        #close the file once transfer is complete
        file.close()
        end = time.time()
        print("Finished running download of ledger in %.2f seconds" %  float(end - start))

    # Server responded with an error
    else:
        print("Something went wrong while getting the ledger.")
        s.close()
        return

    s.close()



    # update ledger with ip of client and public key
    ledger.add_node(helper.find_ip(), pubkey)

    # send updated ledger to all serversin the network
    update_ledger()


#
# Sends a request to server for updating the ledger
#
def update_ledger():

    # logging
    print("******************************")
    print("******************************")
    print("Beginning to send updated ledger to all servers")

    # going through all the ips
    for ip in ledger.get_ips():

        # get the key of the server we want to send to
        serverPubkey = ledger.get_pubkey(ip)

        # run the client
        s = run_client(ip)

        # create a push request for the server and encode it to bytes
        cmd = "update_ledger ledger.json"
        encryptedCmd = encryption.encrypt_using_public_key(cmd.encode(), serverPubkey)
        s.send(encryptedCmd)

        # recieve response from server
        recv = s.recv(REQUEST_MAX_LENGTH).decode()

        # check if the servor responded with an error
        if(recv.split(' ', 1)[0] != "Error"):

            # opening a file
            f = open(ledger.LEDGER_PATH, 'rb')

            # read bytes and set up counter "byte"
            l = f.read(BYTES_TO_SEND)
            byte = BYTES_TO_SEND

            # a forever loop untill file gets sent
            while (l):

                # encrypt the data with the pubkey of the server
                encrypted_l = encryption.encrypt_using_public_key(l, serverPubkey)

                # send the bytes
                s.send(encrypted_l)

                # read more bytes and incrementing counter
                l = f.read(BYTES_TO_SEND)
                byte += BYTES_TO_SEND

            print(byte, "bytes sent")

        # server did respond with error
        else:
            print("Something went wrong while updating the ledger to", recv)

    print("Finished sending the ledger to everyone")
    print("******************************")
    print("******************************")

def load_balance():

    # logging
    print("******************************")
    print("******************************")
    print("Beginning load balancing ")

    # going through each ip
    for ip in ledger.get_ips():

        # get the key of the server we want to send to
        serverPubkey = ledger.get_pubkey(ip)

        # run the client
        s = run_client(ip)

        # create a push request for the server and encode it to bytes
        cmd = "load_balance garbage"
        encryptedCmd = encryption.encrypt_using_public_key(cmd.encode(), serverPubkey)
        s.send(encryptedCmd)

        # recieve response from server
        recv = s.recv(REQUEST_MAX_LENGTH).decode()

        # check if the servor responded with an error
        if(recv.split(' ', 1)[0] != "Error"):

            recv = s.recv(REQUEST_MAX_LENGTH).decode()

            if(recv.split(' ', 1)[0] != "Error"):
                print()

            # server did respond with error
            else:
                print("Something went wrong while sending a load balance request", s.gethostname())

    print("Finished load balancing")
    print("******************************")
    print("******************************")

#
# Creates a new network with the IP of the client as the first node
#
def start_network():

    # create a private key on the local host and its public key for the ledger
    pubkey = encryption.create_keys()

    # clean the directory for a fresh network
    helper.clean_directory()

    # create the first node in the ledger
    ledger.add_first_node(helper.find_ip(), pubkey)

#
# Deals with creating the client node as well as providing the main command line interface for the program
#
def main():

    pubKey = "MIGJAoGBAIyRlQ56E/7rsQmsulYp/2+FOMd3/B11wOY7WP0blJUaO1mBJwUSKWs0\nFCr49jbc2g1LROCENXS864IQozcS3Z+o+VKPd/oGnwnhx0PXIBhPaQ3o/b9Hm8nu\ndHakdI1nnu7rq5gug068tNK/L00BBWVtsTGHHfs1ClOvkoShZSSFAgMBAAE="

    try:

        if(sys.argv[1] == "push"):
            send_file(sys.argv[2])
        elif(sys.argv[1] == "pull"):
            receive_file(sys.argv[2])
        elif(sys.argv[1] == "pull_ledger"):
            pull_ledger(sys.argv[2], pubKey)
        elif(sys.argv[1] == "update_ledger"):
            update_ledger()
        elif(sys.argv[1] == "start_network"):
            start_network()
        elif(sys.argv[1] == "load_balance"):
            load_balance()
        else:
            print("Unrecognized command entered")

    except:
        print("Oopsies")

main()
