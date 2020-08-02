# NAS: A Decentralized P2P File System
###### A project by Neil Arakkal, Aakaash Kapoor, and Sutej Kulkarni

</br>
</br>

NAS is a decentralized peer to peer file system that focuses on storage efficiency. This allows members of our network to shard and store their files across all the nodes in our network to allow symmetric growth of storage across all nodes. All of the communication between nodes and all the files that are stored across the network are encrypted for security. The network can be accessed using a GUI software, or using command line access.

#### Installation:

* You will need to install the PyQt5 and the PySide2 libraries for Python in order to run the GUI:
      
      pip3 install PyQt5
      pip3 install PySide2

* Clone this repository using:
      
      git clone https://github.com/ECS-251-W2020/final-project-nas.git

* Run the network using:
      
      python3 NAS.py

This should open up the NAS GUI which will allow you to create a new network or join an existing network. In order to join an existing network, you will need access to the IP address of any node in the network and their public key. Once you have joined or created a network, you can then push all of your files to the network and pull them back whenever you need to.

#### Command line access for load balancing:

Files are only sharded and spread across the network based on the current number of nodes present in the system. If nodes are added into the network, this defeats our goal of symmetric storage growth. This is why there is a back door access for administrators to perform load balancing on the network whenever necessary, which will redistribute all the sharded files accounting for the new nodes in the network. The following command can be used in order to run load balancing.

      python3 client.py load_balance

This sends out a request to all the nodes to start load balancing, where each of the nodes start pulling all of their files from the network and push them back into the network.

Side Note:
This process takes time and puts strain on the internet connection due the large restructuring of the network, so it must be performed when the internet connection is not being used. Also, this command must only be accessible by certain personnel in the network, as this can be misused.


#### Basic Architecture

Each host computer running our network is called a node. Each node comprises of clients and a server.

Clients are generated with each action performed in the network (ex: pushing or pulling a file, joining a network, etc.) A client normally has the task of sending out requests to either a single server, or to multiple servers.

The server is constantly running in the background and accepts requests made by clients. The server is designed to have multithreaded sockets which means that it can run multiple requests at the same time. This allows concurrent reads to occur in the network. Each server also has supports for locks during a write. Servers can be locked so that only a single write can occur in the network at a given time.


#### Ledgers

Our network keeps track of its own current state by using a system of ledgers. A ledger is JSON file that contains important information such as the nodes in our network with their IPs and their files files stored. An example of the structure of the ledger is as follows.

    {
        "Nodes": [
            {
                "IP": "10.0.0.5",
                "Key": "MIGJAoGBAJexVGq4OZYd7PC833A...
            },
            ...
        ],
        "Files": [
            {
                "Filename": "HarryPotterMeme.mp4",
                "Owner IP": "10.0.0.160",
                "Shards": [
                    "10.0.0.5",
                    "10.0.0.160",
                    "10.0.0.31"
                ]
            },
            ...
        ]
    }


#### Server and Client API

Since each portion of our network depends upon client and server interaction, both the APIs had to be built out simultaneously. The basic format for communication between a server and client is as follows.

* A client sends a request for an action to a server. The request is encrypted using the server's public key for security.
* The server responds back with either a confirmation, or an error.
* The server then either receives data or sends out data depending on the request.
* The server then sends out a final confirmation saying that the task was completed.

`client.start_network()` : Starts up the network, creating a new ledger and adding the host node into it and creating apair of public and private keys for the node.

`client.pull_ledger() and server.send_ledger()` : This is the method for a node to join an existing network. The client first encrypts a pull_ledger command with a server's public key and sends it to that server. The client then generates a new set of keys and sends the server its own public key. The server then proceeds to encrypt its ledger with the clients public key and sends it back to the client.

`client.update_ledger() and server.update_ledger()` : A method for updating the ledger across all the nodes present in the network. The client will update the ledger with either itself added as a new node when joining an existing netowrk, or will add a new file into the ledger. A call of this function also releases any locks present on the server.

`client.receive_file() and server.send_file()` : The client sends a read request to all the servers that currently store a shard of the file. The servers then start sending out the file shards back to the client. The client finally decrypts the shards using its own public key and combines them back into a file.

`client.lock_servers() and server.lock_server()` : The client sends out a lock request to all the servers, which will then lock them for further writes. If another lock is currently in place by another client, then the client will keep trying to lock the server until it succeeds. The server also keeps track of which node currently locked it.

`client.send_file() and server.receive_file()` : The client first starts out by sending a lock request to all the servers. This prevents other writes from occuring at the same time. The client then shards the file it wants to send and encrypts the shards using its own private key. This step prevents other nodes from reading the shards. The client then sends out the shards to all the servers currently in the network. The client finally adds the new file into the ledger and calls the update_ledger() method which procedurally releases the lock on all the servers.

`client.load_balance() and server.load_balance()` : The load balance method is a method that can only be called from the command line (see above for instructions). The client sends out a load balance request to all the servers one at a time. Each server then proceeds to pull all of its files from the network and then pushes them back into the network. This allows the shards to be redistributed among new members of the network. The server then sends the client a confirmation that load balance has completed.
