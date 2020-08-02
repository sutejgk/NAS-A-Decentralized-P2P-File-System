serverLock = ""

#
# Acquire the lock and store the ip of the lock holder in the global variable
#
def acquire(ip):
    global serverLock
    serverLock = ip

#
# Check if the lock is currently locked
#
def locked():
    global serverLock

    if serverLock == "":
        return False
    else:
        return True

#
# Check if the lock is currently unlocked
#
def unlocked():
    global serverLock

    if serverLock == "":
        return True
    else:
        return False

#
# Release the lock and make the server available again
#
def release():
    global serverLock
    serverLock = ""

#
# Check if the ip is the current lock holder
#
def check_lock(ip):
    global serverLock
    if ip == serverLock:
        return True
    else:
        return False

#
# Return the IP of the current lock holder
#
def return_lock():
    global serverLock
    return serverLock
