from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget, QLabel)
#from PyQt5.QTGui import QPixmap
import PyQt5.QtWidgets
import sys 
import os
import subprocess
import client 
#import encryption
#import helperFunctions as helper
#import ledgerFunctions as ledger

class WidgetGallery(QDialog):
    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)
        
        self.originalPalette = QApplication.palette()

        styleComboBox = QComboBox()
        styleComboBox.addItems(QStyleFactory.keys())

        #self.createTopLeftGroupBox()
        self.createTopRightGroupBox()
        #self.createBottomLeftTabWidget()
        self.createBottomRightGroupBox()

        styleComboBox.activated[str].connect(self.changeStyle)

        topLayout = QHBoxLayout()
        #topLayout.addWidget(styleLabel)
        #topLayout.addWidget(styleComboBox)
        topLayout.addStretch(1)
        #topLayout.addWidget(self.useStylePaletteCheckBox)

        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        #mainLayout.addWidget(self.topLeftGroupBox, 2, 1)
        mainLayout.addWidget(self.topRightGroupBox, 1, 1)
        #mainLayout.addWidget(self.bottomLeftTabWidget, 2, 0)
        mainLayout.addWidget(self.bottomRightGroupBox, 1, 0)
       #mainLayout.addWidget(self.progressBar, 3, 0, 1, 2)
        mainLayout.setRowStretch(5, 1)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)

        self.setWindowTitle("Welcome to NAS")
        self.changeStyle('Macintosh')

    def changeStyle(self, styleName):
        QApplication.setStyle(QStyleFactory.create(styleName))
        self.changePalette()

    def changePalette(self):
        QApplication.setPalette(self.originalPalette)


    def createBottomRightGroupBox(self):
        self.bottomRightGroupBox = QGroupBox("Enter Server IP address and Public key:")

        self.ip_input = QLineEdit('')
        self.ip_input.setEchoMode(QLineEdit.Normal)

        self.server_public_key_input = QLineEdit('')
        self.server_public_key_input.setEchoMode(QLineEdit.Normal)

        flatPushButton = QPushButton("Thank you for choosing NAS!")
        flatPushButton.setFlat(True)

        layout = QGridLayout()
        layout.addWidget(self.ip_input, 0, 0, 1, 2)
        layout.addWidget(self.server_public_key_input, 2, 0, 1, 2)
        layout.addWidget(flatPushButton, 4, 0, 1, 2)
        layout.setRowStretch(5, 1)
        self.bottomRightGroupBox.setLayout(layout)

    #function for closing the GUI
    def exit_GUI(self):
        print("GUI closed")
        #sys.exit()
        self.close()
    
    #function for calling another python script
    def call_client(self):
        subprocess.call("ls",shell=True)

    # function to open the file browser
    def open_fileBrowser(self):
        subprocess.call("python3 fileBrowser.py",shell=True)

    # Enables the user to connect to the network, takes inputs from ip_input and server_public_key_input
    def join_the_network(self):
            pubKey = str(self.server_public_key_input.text()).replace("\\n", "\n")
            client.pull_ledger(self.ip_input.text(), pubKey)
            self.exit_GUI()
            # self.open_fileBrowser()
    
    # Enables the user to create and start the NAS network, and closes the NAS_GUI
    def start_my_network(self):
            client.start_network()
            self.exit_GUI()
            # self.open_fileBrowser()
            #print("Hey there!")

    #Just a check to see if text input gets printed when we click join the network
    def check_text(self):
        y = self.ip_input.text()
        print(y)
        print(self.server_public_key_input.text())

        #function for creating top right box(submit and quit buttons)
    def createTopRightGroupBox(self):
        self.topRightGroupBox = QGroupBox("NAS network options")
        
        #When a user clicks this button "join_the_network" function is called
        join_nas_network_button = QPushButton("Join the network")
        join_nas_network_button.clicked.connect(self.join_the_network)
        
        #When a user clicks this button, GUI closes
        quit_button = QPushButton("Quit")
        quit_button.clicked.connect(self.exit_GUI)

        # When a user clicks this button, "start_my_network" function is called
        create_nas_network_button = QPushButton("Create my network")
        create_nas_network_button.clicked.connect(self.start_my_network)

        layout = QVBoxLayout()
        layout.addWidget(join_nas_network_button)
        layout.addWidget(quit_button)
        layout.addWidget(create_nas_network_button)
        layout.addStretch(1)
        self.topRightGroupBox.setLayout(layout)


if __name__ == '__main__':

    import sys

    #app = QApplication(sys.argv)
    app = QApplication([])
    #print(PyQt5.QtWidgets.QStyleFactory.keys())
    gallery = WidgetGallery()
    gallery.show()
    sys.exit(app.exec_())
