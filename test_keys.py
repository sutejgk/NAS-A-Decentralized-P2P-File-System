from cryptography.fernet import Fernet

def create_and_store_keys():
    #Create public key 
    public_key = Fernet.generate_key()
    pubk_string = str(public_key)
    #print to check whether key is valid
    print(public_key)
    #Create private key
    private_key = Fernet.generate_key()
    prik_string = str(private_key)
    #print to check whether key is valid
    print(private_key)

    # Creates a new empty file called private.key 
    with open('private.key', 'w') as fp: 
        pass
    #Copies its private key into the private.key file
    with open('private.key', 'w') as filehandle:
        for character in prik_string:
            filehandle.write('%s' % character)
            
    # Creates a new empty file called public.key 
    with open('public.key', 'w') as fp: 
        pass
    #Copies its public key into the public.key file
    with open('public.key', 'w') as filehandle:
        for character in pubk_string:
            filehandle.write('%s' % character)

create_and_store_keys() 
