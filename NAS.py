import subprocess
from pathlib import Path
LEDGER_PATH = "ledger.json"

# function to open the NAS GUI to enable the user to connect to the network
def open_NAS_GUI():
        subprocess.call("python3 NAS_GUI.py",shell=True)
        main()

# function to open the file browser
def open_fileBrowser():
        subprocess.call("python3 fileBrowser.py",shell=True)



my_file = Path(LEDGER_PATH)

# If ledger exists on your system, that means you are connected to the network,
# will directly open the file browser.
# If ledger does not exist on your system, NAS GUI will open and help you get 
# connected to the network.
def main():
	if my_file.is_file():
		open_fileBrowser()
	else:
		open_NAS_GUI()

main()
