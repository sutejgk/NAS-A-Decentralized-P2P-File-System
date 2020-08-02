import rsa
from textwrap import wrap
import helperFunctions as helper

PRIVATE_KEY_PATH = "private_key.pem"
MESSAGE_CHUNK_LIMIT = 100
ENCRYPTION_BYTE_LIMIT = 128

# Creates private and public keys for a node in the network and stores these
# keys on the local machine in PEM formats
def create_keys():

    #Creates new keys, public and private key
    (servers_pubkey, servers_privkey) = rsa.newkeys(1024)

    # Saves private and public keys on local machine in PEM format
    priv_key_file = open(PRIVATE_KEY_PATH, 'wb')
    priv_key_file.write(servers_privkey.save_pkcs1())
    priv_key_file.close()

    pubkey = servers_pubkey.save_pkcs1().decode()[31:-30]

    return pubkey

# Performs encryption a message usign a provided public key
def encrypt_using_public_key(data,public_key):

    public_key = "-----BEGIN RSA PUBLIC KEY-----\n" + public_key + \
                "\n-----END RSA PUBLIC KEY-----\n"
    #print(public_key)
    my_final_public_key = rsa.PublicKey.load_pkcs1(public_key)

    # #split data into equally sized chunks
    # message_split = helper.split_data_chunk_size(data, MESSAGE_CHUNK_LIMIT)
    message_split = []

    # #create an empty byte string for encrypted message
    encrypted_message = b''

    for message in message_split:
        
        #client encrypts its linux command using servers public key
        encrypted_message += rsa.encrypt(message, my_final_public_key)

    return data

#Performs decryption on an encrypted message when keys
#are present locally on a machine
# byte -> byte
def decrypt_using_private_key(encrypted_message):


    # #Read the private key stored in secondary memory in PEM format
    with open(PRIVATE_KEY_PATH, mode='rb') as privatefile:
        private_key_data = privatefile.read()

    # #Convert the PEM format to normal private key format
    my_final_private_key = rsa.PrivateKey.load_pkcs1(private_key_data)

    # message_split = helper.split_data_chunk_size(encrypted_message, ENCRYPTION_BYTE_LIMIT)
    message_split = []

    decrypted_message = b''

    for message in message_split:
        #server decrypts it using its own private key
        decrypted_message += rsa.decrypt(message,my_final_private_key)

    # return decrypted_message
    return encrypted_message
