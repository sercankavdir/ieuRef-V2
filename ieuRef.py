import sys
from msilib import Dialog

import bibtexparser
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from PyQt5 import QtCore
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
import csv

from bibtexparser.bparser import BibTexParser


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowIcon(QIcon('icon/logo.png'))
        file_menu = self.menuBar().addMenu("&File")

        help_menu = self.menuBar().addMenu("&About")
        self.setWindowTitle("IeuRef")
        self.setMinimumSize(1000, 800)
        MainWindow.data = []
        self.tableWidget = QTableWidget()
        self.setCentralWidget(self.tableWidget)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setColumnWidth(0, 300)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.tableWidget.setHorizontalHeaderLabels(("Author", "Year", "Type", "Title"))

        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        statusbar = QStatusBar()
        self.setStatusBar(statusbar)

        selectBibtex_action = QAction(QIcon("icon/addBibtex.png"), "Select BibTeX file", self)
        selectBibtex_action.triggered.connect(self.selectBibtex)
        file_menu.addAction(selectBibtex_action)

        createBibtex_action = QAction(QIcon("icon/create.png"), "Create Bibtex", self)
        createBibtex_action.triggered.connect(self.createBibtex)
        file_menu.addAction(createBibtex_action)

        searchBibtex_action = QAction(QIcon("icon/search.png"), "Search Student", self)
        searchBibtex_action.triggered.connect(self.search)
        file_menu.addAction(searchBibtex_action)

        deleteAllBibtex_action = QAction(QIcon("icon/delete.png"), "Delete All", self)
        deleteAllBibtex_action.triggered.connect(self.deleteAllBibtex)
        file_menu.addAction(searchBibtex_action)

        filterBibtex_action = QAction(QIcon("icon/filterBibtex.png"), "Filter BibTeX ", self)
        filterBibtex_action.triggered.connect(self.filterBibtex)
        file_menu.addAction(filterBibtex_action)

        # Create Author Identity file menu button
        createAuthorIdentityBibtex_action = QAction(QIcon("icon/identity.png"), "Create Author Identity", self)
        createAuthorIdentityBibtex_action.triggered.connect(self.createAuthorIdentity)
        file_menu.addAction(createAuthorIdentityBibtex_action)

        btn_selectBibtex_action = QAction(QIcon("icon/addBibtex.png"), "Select BibTeX file", self)
        btn_selectBibtex_action.triggered.connect(self.selectBibtex)
        btn_selectBibtex_action.setStatusTip('Select BibTeX File')
        toolbar.addAction(btn_selectBibtex_action)

        btn_createBibtex_action = QAction(QIcon("icon/create.png"), "Create Bibtex", self)
        btn_createBibtex_action.triggered.connect(self.createBibtex)
        btn_createBibtex_action.setStatusTip('Create BibTeX Entry')
        toolbar.addAction(btn_createBibtex_action)

        btn_searchBibtex_action = QAction(QIcon("icon/search.png"), "Search Student", self)
        btn_searchBibtex_action.triggered.connect(self.search)
        btn_searchBibtex_action.setStatusTip('Search')
        toolbar.addAction(btn_searchBibtex_action)

        btn_filterBibtex_action = QAction(QIcon("icon/filterBibtex.png"), "Filter BibTeX ", self)
        btn_filterBibtex_action.triggered.connect(self.filterBibtex)
        btn_filterBibtex_action.setStatusTip('Filter BibTeX')
        toolbar.addAction(btn_filterBibtex_action)

        # Create Author Identity button on the main screen with its icon
        btn_createAuthorIdentityBibtex_action = QAction(QIcon("icon/identity.png"), "Create Author Identity", self)
        btn_createAuthorIdentityBibtex_action.triggered.connect(self.createAuthorIdentity)
        btn_createAuthorIdentityBibtex_action.setStatusTip('Create Author Identity')
        toolbar.addAction(btn_createAuthorIdentityBibtex_action)


        btn_deleteAllBibtex_action = QAction(QIcon("icon/delete.png"), "Delete All", self)
        btn_deleteAllBibtex_action.triggered.connect(self.deleteAllBibtex)
        btn_deleteAllBibtex_action.setStatusTip('Delete All')
        toolbar.addAction(btn_deleteAllBibtex_action)

    def loaddata(self, keyys):
        MainWindow.data = MainWindow.data + keyys   # append(entry)
        # newData = [(author, year, type1, title)]
        # entry = MainWindow.data
        # entry.append((author, year, type1, title))
        # print("------------------")
        # print(entry)
        self.printData(keyys)

    def printData(self, data):
        # numrows = len(data)  # 6 rows in your example
        # numcols = len(data[0])
        # Printing data to the QTableWidget
        row = self.tableWidget.rowCount()
        for item in data:
            self.tableWidget.insertRow(row)
            self.tableWidget.setItem(row, 0, QTableWidgetItem(item["author"]))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(item["year"]))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(item["ENTRYTYPE"]))
            self.tableWidget.setItem(row, 3, QTableWidgetItem(item["title"]))
            row = row + 1
        # for row in range(numrows):
        #     print(numrows)
        #     self.tableWidget.insertRow(row)
        #     for column in range(numcols):
        #         print(column)
        #         self.tableWidget.setItem(row, column, QTableWidgetItem((data[row][column])))


    def createBibtex(self):
        dlg = CreateDialog()
        dlg.exec_()

    def search(self):
        dlg = SearchDialog()
        # dlg.exec_()
        # if dlg.accepted():
        s = dlg.searchString
        for item in MainWindow.data:
            for k, v in item.items():
                if s in v:
                    print("found: " + v)

    def filterBibtex(self):
        dlg = FilterDialog()
        dlg.exec_()

    def deleteAllBibtex(self):
        self.MainWindow.data.clear()
        self.printData(MainWindow.data)

    def createAuthorIdentity(self):
        dlg = CreateAuthorIdentityDialog()
        dlg.exec_()

    def selectBibtex(self):
        options = QFileDialog.Options()
        bibtexFile, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                    "BibTeX Files (*.bib)", options=options)
        if(bibtexFile):
            with open(bibtexFile) as bibtex:

                try:
                    parser = BibTexParser(common_strings=False)
                    parser.ignore_nonstandard_types = False
                    parser.homogenise_fields = False
                    bibtex_database = bibtexparser.load(bibtex)
                    keyys = bibtex_database.entries
                    countEntry = len(keyys)
                    self.loaddata(keyys)

                except Exception:
                    print(format(Exception))
                    QMessageBox.warning(QMessageBox(), 'Error', 'Could not load Bibtex file.')
        else:
            return

class CreateDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(CreateDialog, self).__init__(*args, **kwargs)

        self.setWindowTitle("Add New ")
        self.setFixedWidth(600)
        self.setFixedHeight(300)

        self.setWindowTitle("Create New BibTeX file")
        self.setFixedWidth(300)
        self.setFixedHeight(100)

        self.boxlabel = QLabel("Entry Type:")

        layout = QFormLayout()
        self.typeinput = QComboBox()
        self.typeinput.addItem("-Please select a BibTeX file type")
        self.typeinput.addItem("Article")
        self.typeinput.addItem("Book")
        self.typeinput.addItem("Journal")
        self.typeinput.addItem("Proceeding")
        self.typeinput.addItem("InProceeding")
        self.typeinput.addItem("MasterThesis")
        self.typeinput.addItem("PhdThesis")
        self.typeinput.addItem("Unpublished")
        self.typeinput.addItem("Misc")
        self.typeinput.activated[str].connect(self.selected)

        layout.addWidget(self.boxlabel)
        layout.addWidget(self.typeinput)
        self.setLayout(layout)

    def selected(self, data):
        if data == "Article":
            dlc = Article()
            dlc.exec_()
        if data == "Book":
            dlc = Book()
            dlc.exec_()
        if data == "Journal":
            dlc = Journal()
            dlc.exec_()
        if data == "Proceeding":
            dlc = Proceeding()
            dlc.exec_()
        if data == "InProceeding":
            dlc = InProceeding()
            dlc.exec_()
        if data == "MasterThesis":
            dlc = MasterThesis()
            dlc.exec_()
        if data == "PhdThesis":
            dlc = PhdThesis()
            dlc.exec_()
        if data == "Unpublished":
            dlc = Unpublished()
            dlc.exec_()
        if data == "Misc":
            dlc = Misc()
            dlc.exec_()


class Article(QDialog):
    def __init__(self, *args, **kwargs):
        super(Article, self).__init__(*args, **kwargs)

        self.setWindowTitle("Article")
        self.setFixedWidth(400)
        self.setFixedHeight(400)

        self.createButton = QPushButton("Create")

        self.line1 = QLineEdit()
        self.line2 = QLineEdit()
        self.line3 = QLineEdit()
        self.line4 = QLineEdit()
        self.line5 = QLineEdit()
        self.line6 = QLineEdit()

        self.text1 = QLabel("Author:")
        self.text2 = QLabel("BibTeXKey:")
        self.text3 = QLabel("Title:")
        self.text4 = QLabel("Year:")
        self.text5 = QLabel("ID:")
        self.text6 = QLabel("Journal:")

        layout = QVBoxLayout()
        layout.addWidget(self.text1)
        layout.addWidget(self.line1)
        layout.addWidget(self.text2)
        layout.addWidget(self.line2)
        layout.addWidget(self.text3)
        layout.addWidget(self.line3)
        layout.addWidget(self.text4)
        layout.addWidget(self.line4)
        layout.addWidget(self.text5)
        layout.addWidget(self.line5)
        layout.addWidget(self.text6)
        layout.addWidget(self.line6)
        layout.addWidget(self.createButton)
        self.createButton.clicked.connect(self.btn_clk)
        self.setLayout(layout)

    def btn_clk(self):
        author = self.line1.text()
        bibtexkey = self.line2.text()
        title = self.line3.text()
        year = self.line4.text()
        ID = self.line5.text()
        journal = self.line6.text()

        newfile = open(str(bibtexkey) + ".bib", "w")
        newfile.write(
            "@" + "article" + "{" + str(bibtexkey) + "," + "\nAuthor=" + author + "\nYear=" + str(
                year) + "\nTitle=" + title + "\n journal=" + journal + "\n ID=" + str(ID) + "\n}")

        newfile.close()


class Book(QDialog):
    def __init__(self, *args, **kwargs):
        super(Book, self).__init__(*args, **kwargs)
        self.setWindowTitle("Book")
        self.setFixedWidth(400)
        self.setFixedHeight(400)

        self.createButton = QPushButton("Create")

        self.line1 = QLineEdit()
        self.line2 = QLineEdit()
        self.line3 = QLineEdit()
        self.line4 = QLineEdit()
        self.line5 = QLineEdit()
        self.line6 = QLineEdit()

        self.text1 = QLabel("Author:")
        self.text2 = QLabel("BibTeXKey:")
        self.text3 = QLabel("Title:")
        self.text4 = QLabel("Year:")
        self.text5 = QLabel("ID:")
        self.text6 = QLabel("Publisher:")

        layout = QVBoxLayout()
        layout.addWidget(self.text1)
        layout.addWidget(self.line1)
        layout.addWidget(self.text2)
        layout.addWidget(self.line2)
        layout.addWidget(self.text3)
        layout.addWidget(self.line3)
        layout.addWidget(self.text4)
        layout.addWidget(self.line4)
        layout.addWidget(self.text5)
        layout.addWidget(self.line5)
        layout.addWidget(self.text6)
        layout.addWidget(self.line6)
        layout.addWidget(self.createButton)
        self.createButton.clicked.connect(self.btn_clk)
        self.setLayout(layout)

    def btn_clk(self):
        author = self.line1.text()
        bibtexkey = self.line2.text()
        title = self.line3.text()
        year = self.line4.text()
        ID = self.line5.text()
        publisher = self.line6.text()

        newfile = open(str(bibtexkey) + ".bib", "w")
        newfile.write(
            "@" + "book" + "{" + str(bibtexkey) + "," + "\nAuthor=" + author + "\nYear=" + str(
                year) + "\nTitle=" + title + "\n publisher=" + publisher + "\n ID=" + str(ID) + "\n}")

        newfile.close()


class Journal(QDialog):
    def __init__(self, *args, **kwargs):
        super(Journal, self).__init__(*args, **kwargs)
        self.setWindowTitle("Journal")
        self.setFixedWidth(400)
        self.setFixedHeight(400)

        self.createButton = QPushButton("Create")

        self.line1 = QLineEdit()
        self.line2 = QLineEdit()
        self.line3 = QLineEdit()
        self.line4 = QLineEdit()
        self.line5 = QLineEdit()

        self.text1 = QLabel("Author:")
        self.text2 = QLabel("BibTeXKey:")
        self.text3 = QLabel("Title:")
        self.text4 = QLabel("Year:")
        self.text5 = QLabel("ID:")

        layout = QVBoxLayout()
        layout.addWidget(self.text1)
        layout.addWidget(self.line1)
        layout.addWidget(self.text2)
        layout.addWidget(self.line2)
        layout.addWidget(self.text3)
        layout.addWidget(self.line3)
        layout.addWidget(self.text4)
        layout.addWidget(self.line4)
        layout.addWidget(self.text5)
        layout.addWidget(self.line5)
        layout.addWidget(self.createButton)
        self.createButton.clicked.connect(self.btn_clk)
        self.setLayout(layout)

    def btn_clk(self):
        author = self.line1.text()
        bibtexkey = self.line2.text()
        title = self.line3.text()
        year = self.line4.text()
        ID = self.line5.text()

        newfile = open(str(bibtexkey) + ".bib", "w")
        newfile.write(
            "@" + "journal" + "{" + str(bibtexkey) + "," + "\nAuthor=" + author + "\nYear=" + str(
                year) + "\nTitle=" + title + "\n ID=" + str(ID) + "\n}")

        newfile.close()


class Proceeding(QDialog):
    def __init__(self, *args, **kwargs):
        super(Proceeding, self).__init__(*args, **kwargs)
        self.setWindowTitle("Proceeeding")
        self.setFixedWidth(400)
        self.setFixedHeight(200)

        self.createButton = QPushButton("Create")

        self.line1 = QLineEdit()
        self.line2 = QLineEdit()

        self.text1 = QLabel("Title:")
        self.text2 = QLabel("Year:")

        layout = QVBoxLayout()
        layout.addWidget(self.text1)
        layout.addWidget(self.line1)
        layout.addWidget(self.text2)
        layout.addWidget(self.line2)
        layout.addWidget(self.createButton)
        self.createButton.clicked.connect(self.btn_clk)
        self.setLayout(layout)

    def btn_clk(self):
        title = self.line1.text()
        year = self.line2.text()

        newfile = open("Proceeding.bib", "w")
        newfile.write(
            "@" + "proceeding" + "{" "\nYear=" + str(year) + "\nTitle=" + title + "\n}")

        newfile.close()


class InProceeding(QDialog):
    def __init__(self, *args, **kwargs):
        super(InProceeding, self).__init__(*args, **kwargs)
        self.setWindowTitle("InProceeding")
        self.setFixedWidth(400)
        self.setFixedHeight(400)

        self.createButton = QPushButton("Create")

        self.line1 = QLineEdit()
        self.line2 = QLineEdit()
        self.line3 = QLineEdit()
        self.line4 = QLineEdit()
        self.line5 = QLineEdit()
        self.line6 = QLineEdit()

        self.text1 = QLabel("Author:")
        self.text2 = QLabel("BibTeXKey:")
        self.text3 = QLabel("Title:")
        self.text4 = QLabel("Year:")
        self.text5 = QLabel("ID:")
        self.text6 = QLabel("Book Title:")

        layout = QVBoxLayout()
        layout.addWidget(self.text1)
        layout.addWidget(self.line1)
        layout.addWidget(self.text2)
        layout.addWidget(self.line2)
        layout.addWidget(self.text3)
        layout.addWidget(self.line3)
        layout.addWidget(self.text4)
        layout.addWidget(self.line4)
        layout.addWidget(self.text5)
        layout.addWidget(self.line5)
        layout.addWidget(self.text6)
        layout.addWidget(self.line6)
        layout.addWidget(self.createButton)
        self.createButton.clicked.connect(self.btn_clk)
        self.setLayout(layout)

    def btn_clk(self):
        author = self.line1.text()
        bibtexkey = self.line2.text()
        title = self.line3.text()
        year = self.line4.text()
        ID = self.line5.text()
        booktitle = self.line6.text()

        newfile = open(str(bibtexkey) + ".bib", "w")
        newfile.write(
            "@" + "inproceeding" + "{" + str(bibtexkey) + "," + "\nAuthor=" + author + "\nYear=" + str(
                year) + "\nTitle=" + title + "\n book title=" + booktitle + "\n ID=" + str(ID) + "\n}")

        newfile.close()


class MasterThesis(QDialog):
    def __init__(self, *args, **kwargs):
        super(MasterThesis, self).__init__(*args, **kwargs)
        self.setWindowTitle("MasterThesis")
        self.setFixedWidth(400)
        self.setFixedHeight(400)

        self.createButton = QPushButton("Create")

        self.line1 = QLineEdit()
        self.line2 = QLineEdit()
        self.line3 = QLineEdit()
        self.line4 = QLineEdit()
        self.line5 = QLineEdit()
        self.line6 = QLineEdit()

        self.text1 = QLabel("Author:")
        self.text2 = QLabel("BibTeXKey:")
        self.text3 = QLabel("Title:")
        self.text4 = QLabel("Year:")
        self.text5 = QLabel("ID:")
        self.text6 = QLabel("School:")

        layout = QVBoxLayout()
        layout.addWidget(self.text1)
        layout.addWidget(self.line1)
        layout.addWidget(self.text2)
        layout.addWidget(self.line2)
        layout.addWidget(self.text3)
        layout.addWidget(self.line3)
        layout.addWidget(self.text4)
        layout.addWidget(self.line4)
        layout.addWidget(self.text5)
        layout.addWidget(self.line5)
        layout.addWidget(self.text6)
        layout.addWidget(self.line6)
        layout.addWidget(self.createButton)
        self.createButton.clicked.connect(self.btn_clk)
        self.setLayout(layout)

    def btn_clk(self):
        author = self.line1.text()
        bibtexkey = self.line2.text()
        title = self.line3.text()
        year = self.line4.text()
        ID = self.line5.text()
        school = self.line6.text()

        newfile = open(str(bibtexkey) + ".bib", "w")
        newfile.write(
            "@" + "masterthesis" + "{" + str(bibtexkey) + "," + "\nAuthor=" + author + "\nYear=" + str(
                year) + "\nTitle=" + title + "\n school=" + school + "\n ID=" + str(ID) + "\n}")

        newfile.close()


class PhdThesis(QDialog):
    def __init__(self, *args, **kwargs):
        super(PhdThesis, self).__init__(*args, **kwargs)
        self.setWindowTitle("MasterThesis")
        self.setFixedWidth(400)
        self.setFixedHeight(400)

        self.createButton = QPushButton("Create")

        self.line1 = QLineEdit()
        self.line2 = QLineEdit()
        self.line3 = QLineEdit()
        self.line4 = QLineEdit()
        self.line5 = QLineEdit()
        self.line6 = QLineEdit()

        self.text1 = QLabel("Author:")
        self.text2 = QLabel("BibTeXKey:")
        self.text3 = QLabel("Title:")
        self.text4 = QLabel("Year:")
        self.text5 = QLabel("ID:")
        self.text6 = QLabel("School:")

        layout = QVBoxLayout()
        layout.addWidget(self.text1)
        layout.addWidget(self.line1)
        layout.addWidget(self.text2)
        layout.addWidget(self.line2)
        layout.addWidget(self.text3)
        layout.addWidget(self.line3)
        layout.addWidget(self.text4)
        layout.addWidget(self.line4)
        layout.addWidget(self.text5)
        layout.addWidget(self.line5)
        layout.addWidget(self.text6)
        layout.addWidget(self.line6)
        layout.addWidget(self.createButton)
        self.createButton.clicked.connect(self.btn_clk)
        self.setLayout(layout)

    def btn_clk(self):
        author = self.line1.text()
        bibtexkey = self.line2.text()
        title = self.line3.text()
        year = self.line4.text()
        ID = self.line5.text()
        school = self.line6.text()

        newfile = open(str(bibtexkey) + ".bib", "w")
        newfile.write(
            "@" + "phdthesis" + "{" + str(bibtexkey) + "," + "\nAuthor=" + author + "\nYear=" + str(
                year) + "\nTitle=" + title + "\n school=" + school + "\n ID=" + str(ID) + "\n}")

        newfile.close()


class Unpublished(QDialog):
    def __init__(self, *args, **kwargs):
        super(Unpublished, self).__init__(*args, **kwargs)
        self.setWindowTitle("Unpublished")
        self.setFixedWidth(400)
        self.setFixedHeight(250)

        self.createButton = QPushButton("Create")

        self.line1 = QLineEdit()
        self.line2 = QLineEdit()
        self.line3 = QLineEdit()

        self.text1 = QLabel("Author:")
        self.text2 = QLabel("Title:")
        self.text3 = QLabel("Note:")

        layout = QVBoxLayout()
        layout.addWidget(self.text1)
        layout.addWidget(self.line1)
        layout.addWidget(self.text2)
        layout.addWidget(self.line2)
        layout.addWidget(self.text3)
        layout.addWidget(self.line3)
        layout.addWidget(self.createButton)
        self.createButton.clicked.connect(self.btn_clk)
        self.setLayout(layout)

    def btn_clk(self):
        author = self.line1.text()
        title = self.line2.text()
        note = self.line3.text()

        newfile = open("Unpublished.bib", "w")
        newfile.write(
            "@" + "unpublished" + "{," + "\nAuthor=" + author + "\nTitle=" + title + "\n note=" + note + "\n}")

        newfile.close()


class Misc(QDialog):
    def __init__(self, *args, **kwargs):
        super(Misc, self).__init__(*args, **kwargs)
        self.setWindowTitle("Misc")
        self.setFixedWidth(250)
        self.setFixedHeight(100)

        self.createButton = QPushButton("Create")

        self.text1 = QLabel("Click create for creating a misc file")

        layout = QVBoxLayout()
        layout.addWidget(self.text1)
        layout.addWidget(self.createButton)
        self.createButton.clicked.connect(self.btn_clk)
        self.setLayout(layout)

    def btn_clk(self):


        newfile = open("misc.bib", "w")
        newfile.write(
            "@" + "misc" + "{" "\n}")

        newfile.close()

class FilterDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(FilterDialog, self).__init__(*args, **kwargs)

        self.QBtn = QPushButton()
        self.QBtn.setText("Search")

        self.setWindowTitle("Filter")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        self.QBtn.clicked.connect(self.btn_clk)

        layout = QVBoxLayout()

        self.index1input = QComboBox()
        self.index1input.addItem("Author")
        self.index1input.addItem("type")

        layout.addWidget(self.index1input)

        self.index1input = QLineEdit()
        self.index1input.setPlaceholderText("index")
        layout.addWidget(self.index1input)

        self.index2input = QComboBox()
        self.index2input.addItem("Author")
        self.index2input.addItem("type")

        layout.addWidget(self.index2input)

        self.index2input = QLineEdit()
        self.index2input.setPlaceholderText("index")
        layout.addWidget(self.index2input)

        self.index3input = QComboBox()
        self.index3input.addItem("Author")
        self.index3input.addItem("type")

        layout.addWidget(self.index3input)

        self.index3input = QLineEdit()
        self.index3input.setPlaceholderText("index")
        layout.addWidget(self.index3input)

        self.index4input = QLineEdit()
        self.index4input.setPlaceholderText("Year From")
        layout.addWidget(self.index4input)

        self.index5input = QLineEdit()
        self.index5input.setPlaceholderText("Year To")
        layout.addWidget(self.index5input)



        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def btn_clk(self):

        index1 = ""
        index1label = ""
        index2 = ""
        index2label = ""
        index3 = ""
        index3label = ""
        index4 = ""
        index5 = ""

class SearchDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(SearchDialog, self).__init__(*args, **kwargs)
        # Pelinsu Arslan Task
        # Search code will be here
        self.searchString = "Shi"


class CreateAuthorIdentityDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(CreateAuthorIdentityDialog, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.show()

    # Creates UI for Create Author Identity Screen
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(295, 413)
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(40, 20, 211, 231))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(6)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.addItem = QtWidgets.QPushButton(Dialog)
        self.addItem.setGeometry(QtCore.QRect(90, 260, 51, 41))
        self.addItem.setObjectName("Add Item")
        self.removeItem = QtWidgets.QPushButton(Dialog)
        self.removeItem.setGeometry(QtCore.QRect(150, 260, 51, 41))
        self.removeItem.setObjectName("Remove Item")
        self.saveIdentity = QtWidgets.QPushButton(Dialog)
        self.saveIdentity.setGeometry(QtCore.QRect(60, 330, 81, 51))
        self.saveIdentity.setObjectName("Save Identity")
        self.cancelIdentity = QtWidgets.QPushButton(Dialog)
        self.cancelIdentity.setGeometry(QtCore.QRect(160, 330, 81, 51))
        self.cancelIdentity.setObjectName("Cancel Identity")

        # Displays names and characters for components on the screen
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        # Loads author identity data from cvs file
        self.loadAuthorIdentityData()

        # Defines function calls for buttons on the screen
        self.addItem.clicked.connect(self.addNewRow)
        self.removeItem.clicked.connect(self.removeSelectedRow)
        self.saveIdentity.clicked.connect(self.saveAuthorIdentityScreen)
        self.cancelIdentity.clicked.connect(self.close)

    # Displays names of UI components on the screen
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Create Author Identity"))

        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Author"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Variation"))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)

        self.tableWidget.setSortingEnabled(__sortingEnabled)
        self.addItem.setText(_translate("Dialog", "+"))
        self.removeItem.setText(_translate("Dialog", "-"))
        self.saveIdentity.setText(_translate("Dialog", "SAVE"))
        self.cancelIdentity.setText(_translate("Dialog", "CANCEL"))

    # Removes selected rows from the table widget
    def removeSelectedRow(self):
        indices = self.tableWidget.selectionModel().selectedRows()
        for index in sorted(indices):
            self.tableWidget.removeRow(index.row())

    # Adds a new row at the end of the table widget
    def addNewRow(self):
        rowPosition = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowPosition)

    # Saves the current status of the table widget into a csv file
    def saveAuthorIdentityScreen(self):
        # Supports Turkish special characters with UTF-8 encoding
        with open('authorIdentityData.csv', 'w', encoding='UTF-8', newline='') as stream:
            writer = csv.writer(stream, lineterminator='\n')
            for row in range(self.tableWidget.rowCount()):
                rowdata = []
                for column in range(self.tableWidget.columnCount()):
                    item = self.tableWidget.item(row, column)
                    if item is not None:
                        #                        rowdata.append(unicode(item.text()).encode('utf8'))
                        rowdata.append(item.text())  # +
                    else:
                        rowdata.append('')

                writer.writerow(rowdata)

        # Displays SAVED message after Save button is clicked
        msg = QMessageBox()
        QMessageBox.about(msg, "Status", "SAVED")

        # Gets author identity data from csv file and puts the contents into a list
        with open('authorIdentityData.csv', 'r', encoding='UTF-8', newline='') as csv_file:
            authorIdentityData = list(csv.reader(csv_file))
        print(authorIdentityData)

    # Imports author identity data from the csv file into the table widget
    def loadAuthorIdentityData(self):
        # Support Turkish special characters with UTF-8 encoding
        with open('authorIdentityData.csv', 'r', encoding='UTF-8', newline='') as csv_file:
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(2)
            my_file = csv.reader(csv_file, delimiter=',', quotechar='|')
            for row_data in my_file:
                row = self.tableWidget.rowCount()
                self.tableWidget.insertRow(row)
                if len(row_data) > 10:
                    self.tableWidget.setColumnCount(len(row_data))
                for column, stuff in enumerate(row_data):
                    item = QTableWidgetItem(stuff)
                    self.tableWidget.setItem(row, column, item)

app = QApplication(sys.argv)
if (QDialog.Accepted == True):
    window = MainWindow()
    window.show()

sys.exit(app.exec_())
