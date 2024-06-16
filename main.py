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
        self.curr_file = 0

        self.folderPathSelectorButton.clicked.connect(self.select_folder)
        self.fileNameButton.clicked.connect(self.open_file)
        self.addCatButton.clicked.connect(self.add_category)
        self.delCatButton.clicked.connect(self.del_category)
        self.set_amount()

    def set_amount(self):
        '''Sets the amount of files and current file as text of label'''
        self.amountLabel.setText(f'{self.curr_file}/{len(self.files)}')

    def set_filename(self):
        '''Sets the name of file as text of button'''
        self.fileNameButton.setText(f'{self.files[self.curr_file]}')

    def add_btns_for_catsegories(self):
        '''Adds buttons to the grid layout for each category'''
        rows = int(len(self.folders)/7 + 1)
        position = [(i, j) for i in range(rows) for j in range(7)]

        for i in range(self.buttonsGrigLayout.count())[::-1]:
            self.buttonsGrigLayout.itemAt(i).widget().deleteLater()

        for position, category in zip(position, self.folders):
            button = QtWidgets.QPushButton(category)
            lambda_ = self.create_lambda(category)

            button.clicked.connect(lambda_)
            button.setFixedSize(100, 35)
            self.buttonsGrigLayout.addWidget(button, *position)

    def create_lambda(self, category):
        '''Creates lambda function for each button'''
        return lambda: self.move_to_category(category)

    def move_to_category(self, category):
        '''Moves current file to the given category'''
        file_name = self.files[self.curr_file]

        path_to_file = os.path.join(self.folder, file_name)
        path_to_dest = os.path.join(self.folder, category, file_name)

        os.rename(path_to_file, path_to_dest)

        if self.curr_file < len(self.files)-1:
            self.curr_file += 1
            self.display_image()
            self.set_amount()
            self.set_filename()
        else:
            self.reset_state()

    def reset_state(self):
        '''Rests state to initial state'''
        self.folder = None
        self.folders = []
        self.files = []
        self.curr_file = 0
        self.imageLabel.clear()
        self.imageLabel.setText('Nothing here... Just both of us...')
        self.folderPathSelectorButton.setText('Select Folder')
        self.fileNameButton.setText('FileName')
        self.amountLabel.setText('Amount')
        self.catListComboBox.clear()
        self.add_btns_for_catsegories()
        self.catListComboBox.setEditText('New Category Name')

    def display_image(self):
        '''Displays image from the current file in the label'''
        path_to_image = os.path.join(self.folder, self.files[self.curr_file])
        self.imageLabel.setPixmap(QtGui.QPixmap(path_to_image))
        self.imageLabel.show()

    def set_categories(self):
        '''Sets the categories to the folders in the current folder'''
        self.catListComboBox.clear()
        self.catListComboBox.addItems(self.folders)
        self.add_btns_for_catsegories()

    def get_folder_content(self):
        '''Gets the content of current folder'''
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
        self.set_amount()
        self.set_filename()
        self.set_categories()
        self.display_image()

    def add_category(self):
        '''Adds new category with the name of the text of combobox'''
        category = self.catListComboBox.currentText()
        if category in self.folders or not category:
            return
        os.makedirs(os.path.join(self.folder, category))
        self.folders.append(category)
        self.set_categories()

    def del_category(self):
        '''Deletes selected category.
        All files will be returned to the main folder'''
        category = self.catListComboBox.currentText()
        if category not in self.folders or not category:
            return
        delDialogMessage = f'''Are you sure to delete {category} category?
        All files in this category will be moved to main folder'''

        confirmation = QMessageBox.question(
            self, "Delete Category", delDialogMessage,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No)

        if confirmation == QMessageBox.StandardButton.Yes:
            category_path = os.path.join(self.folder, category)

            for file in os.listdir(category_path):
                os.rename(os.path.join(category_path, file),
                          os.path.join(self.folder, file))

            os.rmdir(os.path.join(self.folder, category))
            self.folders.remove(category)
            self.set_categories()

    def select_folder(self):
        '''Opens folder selection dialog and sets the folder path'''
        self.folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if not self.folder:
            return
        self.folderPathSelectorButton.setText(self.folder)
        self.get_folder_content()

    def open_file(self):
        '''Opens selected file in the default program'''
        if self.fileNameButton.text() == "FileName":
            QMessageBox.information(self, "Error",
                                    "Please select a folder first")
            return
        os.startfile(f'{self.folder}/{self.fileNameButton.text()}')


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
