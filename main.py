import os
import sys
from PyQt6 import QtGui, QtWidgets
from PyQt6.QtWidgets import QMessageBox, QFileDialog
from main_window import Ui_mainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_mainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.folder = None
        self.folders = []
        self.files = []
        self.currFile = 0


        self.folderPathSelectorButton.clicked.connect(self.selectFolder)
        self.fileNameButton.clicked.connect(self.openFile)
        self.addCatButton.clicked.connect(self.addCategory)
        self.delCatButton.clicked.connect(self.delCategory)
        self.setAmount()
        
    def setAmount(self):
        self.amountLabel.setText(f'{self.currFile}/{len(self.files)}')
    
    def setFileName(self):
        self.fileNameButton.setText(f'{self.files[self.currFile]}')

    def addButtonsForCategories(self):
        position = [(i, j) for i in range(int(len(self.folders)/7 + 1)) for j in range(7)]
        
        for i in range(self.buttonsGrigLayout.count())[::-1]:
            self.buttonsGrigLayout.itemAt(i).widget().deleteLater()

        for position, category in zip(position, self.folders):
            button = QtWidgets.QPushButton(category)
            lambda_ = self.create_lambda(category)

            button.clicked.connect(lambda_)
            button.setFixedSize(100,35)
            self.buttonsGrigLayout.addWidget(button, *position)

    def create_lambda(self, category):
        return lambda: self.moveToCategory(category)

    def moveToCategory(self, category):
        print(category)
        path_to_file = os.path.join(self.folder, self.files[self.currFile])
        
        path_to_dest = os.path.join(self.folder, category, self.files[self.currFile])

        os.rename(path_to_file, path_to_dest)
        
        if self.currFile < len(self.files)-1:
            self.currFile += 1
            self.displayImage()
            self.setAmount()
            self.setFileName()
        else:
            self.resetState()

    def resetState(self):
        self.folder = None
        self.folders = []
        self.files = []
        self.currFile = 0
        self.imageLabel.clear()
        self.imageLabel.setText('Nothing here... Just both of us...')
        self.folderPathSelectorButton.setText('Select Folder')
        self.fileNameButton.setText('FileName')
        self.amountLabel.setText('Amount')
        self.catListComboBox.clear()
        self.addButtonsForCategories()
        self.catListComboBox.setEditText('New Category Name')


    def displayImage(self):
        path_to_image = os.path.join(self.folder, self.files[self.currFile])
        print(path_to_image)
        self.imageLabel.setPixmap(QtGui.QPixmap(path_to_image))
        self.imageLabel.show()

    def setCategories(self):
        self.catListComboBox.clear()
        self.catListComboBox.addItems(self.folders)
        self.addButtonsForCategories()

    def getFolderContent(self):
        self.files = []
        self.folders = []
        image_formats = ['jpg', 'png', 'jpeg', 'gif', 'bmp',
                         'webp', 'ico', 'tiff', 'tif']
        for item in os.listdir(self.folder):
            if os.path.isfile(os.path.join(self.folder, item)):
                if item.split(".")[-1] in image_formats:
                    self.files.append(item)
            else:
                self.folders.append(item)
        self.setAmount()
        self.setFileName()
        self.setCategories()
        self.displayImage()

        print(f"{len(self.files)} files and {len(self.folders)} folders in {self.folder}")

    def addCategory(self):
        category = self.catListComboBox.currentText()
        if category in self.folders or not category: return
        os.makedirs(os.path.join(self.folder, category))
        self.folders.append(category)
        self.setCategories()

    def delCategory(self):
        category = self.catListComboBox.currentText()
        if category not in self.folders or not category: return
        delDialogMessage = f'Are you sure to delete {category} category?\nAll files in this category will be moved to main folder'
        confirmation = QMessageBox.question(self,"Delete Category", delDialogMessage, QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if confirmation == QMessageBox.StandardButton.Yes:
            for file in os.listdir(os.path.join(self.folder, category)):
                os.rename(os.path.join(self.folder, category, file), os.path.join(self.folder, file))
            os.rmdir(os.path.join(self.folder, category))
            self.folders.remove(category)
            self.setCategories()

    def selectFolder(self):
        self.folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if not self.folder: return
        self.folderPathSelectorButton.setText(self.folder)
        self.getFolderContent()

    def openFile(self):
        if self.fileNameButton.text() == "FileName": 
            QMessageBox.information(self, "Error", "Please select a folder first")
            return
        os.startfile(f'{self.folder}/{self.fileNameButton.text()}')
        



if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())