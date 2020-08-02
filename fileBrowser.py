from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore
import client
import os
import sys

from ui import main

fileNumber= "0"

#
# Class that allows the addition of column we use to provide
# if the file is sharded or not
#
class ExtraColumnModel(QtWidgets.QFileSystemModel):

    # Adds a column to the display
    def columnCount(self, parent = QtCore.QModelIndex()):
        return super(ExtraColumnModel, self).columnCount()+1

    # Sets the name of the column
    def headerData(self, section, o, role):
        if o == QtCore.Qt.Horizontal and section == self.columnCount() - 1:
            return "Sharded"
        return super(ExtraColumnModel, self).headerData(section, o, role)

    # Stores the data to be added to the column
    def data(self, index, role):

        # Filename of the column we need 
        filename = super(ExtraColumnModel, self).data(index, QtWidgets.QFileSystemModel.Roles.FileNameRole)

        # if its the last column
        if index.column() == self.columnCount() - 1:

            # if filename has digit in it at the end
            if role == QtCore.Qt.DisplayRole and filename[-1].isdigit():
                return "True"
            elif role == QtCore.Qt.DisplayRole:
                return "False"

        # if the first column
        elif index.column() == 0:
            if role == QtCore.Qt.DisplayRole and filename[-1].isdigit():
                fileNumber = filename[-1]
                return filename[:-1]

        return super(ExtraColumnModel, self).data(index, role)

#
# Main class that gets all the files and creates context menus for them
# if the file is sharded or not
#
class MyFileBrowser(main.Ui_MainWindow, QtWidgets.QMainWindow):

    # Initialize the class with our custom context menu
    def __init__(self, maya=False):
        super(MyFileBrowser, self).__init__()

        # get the window
        self.window = self.setupUi(self)

        # set up the model
        self.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.context_menu)

        # button set up
        self.btn = QtWidgets.QPushButton('Add File', self)
        self.btn.resize(90,30)
        self.btn.clicked.connect(self.file_picker)
        self.btn.move(self.window.frameGeometry().width() - 120, self.window.frameGeometry().height() - 112)  
        self.populate()


    # Function to pick files from the browser
    def file_picker(self):

        # get the filename 
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Single File', "/Users/aakaashkapoor/Desktop/toSend",'*')[0]
        
        # call the the client read
        client.send_file(filename)

        

    # Populate the UI correctly
    def populate(self):

        # file population to the UI in the current 
        path = "directory"
        self.model = ExtraColumnModel()
        self.model.setRootPath((QtCore.QDir.rootPath()))
        self.treeView.setModel(self.model)

        # changing width of the first column
        self.treeView.setColumnWidth(0, 300)
        self.treeView.setRootIndex(self.model.index(path))

        # files will be sorted
        self.treeView.setSortingEnabled(True)


    # Creates the context munu
    def context_menu(self):

        # sets up the menu
        menu = QtWidgets.QMenu()

        # creates a menu based on the filetype
        filename = self.model.fileName(self.treeView.currentIndex())
        filetype = self.model.type(self.treeView.currentIndex()).split(" ")[0]

        # if file is not present here
        if filetype[-1].isdigit() == True:
            open = menu.addAction("Pull File")
            open.triggered.connect(self.read_file)

        # file exists in the curent system
        else:
            open = menu.addAction("Push File")
            open.triggered.connect(self.write_file)
            open = menu.addAction("Open File")
            open.triggered.connect(self.open_file)

        cursor = QtGui.QCursor()
        menu.exec_(cursor.pos())


    # Should call the file read from the client
    def read_file(self):

        # get the current filename
        filename = self.model.fileName(self.treeView.currentIndex())

        # call the the client read
        client.receive_file(filename)

        # remove the file
        os.remove("directory/" + filename + fileNumber)

    # Should call the file write to client
    def write_file(self):

        # get the current filename
        filename = self.model.fileName(self.treeView.currentIndex())

        # call the the client read
        client.send_file("directory/" + filename)

        # remove the file
        os.remove("directory/" + filename)

    # Should call the file write to client
    def open_file(self):

        # get the current filename
        filename = self.model.fileName(self.treeView.currentIndex())

        # remove the file
        os.system("open directory/" + filename)




if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    fb = MyFileBrowser()
    fb.show()
    app.exec_()