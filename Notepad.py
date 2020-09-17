# This is the working version of our notepad so far. 
# Please see John_workspace.py under John's branch to view 
# a somewhat detailed list of different features and future
# implementation ideas. 

import os, sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QLabel, \
                            QPlainTextEdit, QStatusBar, QToolBar, QVBoxLayout, QAction, \
                            QFileDialog, QMessageBox, QColorDialog, QTextEdit
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QFontDatabase, QIcon, QKeySequence, QColor, QFont, QTextCharFormat
from PyQt5.QtPrintSupport import QPrintDialog
import Folders
import Tabs

# This is our main class, our notepad 
class Notepad(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('./Icons/notepad.png'))
        self.setGeometry(700, 400, 700, 700)

        # These are the types of files our notepad can open/read/use
        self.filterTypes = 'Text Document (*.txt);; Python (*.py);; PDF (*.pdf)'

        # This initializes the path to None so we can tell if we have a new note open
        # or if we are loading up an old note. 
        self.path = None
  
        # Actual Notepad editor (and coloring and font and font size)
        mainLayout = QVBoxLayout()
        self.editor = QTextEdit()
        fixedFont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixedFont.setPointSize(18)
        self.editor.setFont(fixedFont)
        self.setStyleSheet("color: lime; background-color: black; selection-color: white; selection-background-color: blue;")
        mainLayout.addWidget(self.editor)
        self.editor.setAutoFormatting(QTextEdit.AutoAll)

        # Status Bar
        self.statusBar = self.statusBar()

        # App Container
        container = QWidget()
        container.setLayout(mainLayout)
        self.setCentralWidget(container)

        # File Menus
        file_menu = self.menuBar().addMenu('&File')

        # File ToolBar (Bottom)
        file_toolbar = QToolBar('File')
        file_toolbar.setIconSize(QSize(60,60))
        self.addToolBar(Qt.BottomToolBarArea, file_toolbar)

        # Open, Save, SaveAs
        openNote = self.create_action(self, './Icons/open', 'Open File...', 
                                            'Opens a file', self.file_open)
        
        saveNote = self.create_action(self, './Icons/save_file.png', 'Save File',
                                            'Saves the file', self.file_save)                                      
        saveNote.setShortcut(QKeySequence.Save)

        saveNoteAs = self.create_action(self, './Icons/save_as.png', 'Save As...',
                                            'Saves the file as', self.file_saveAs)
        saveNoteAs.setShortcut('Ctrl+Shift+S')

        file_menu.addActions([openNote, saveNote, saveNoteAs])
        file_toolbar.addActions([openNote, saveNote, saveNoteAs])

        # Edit Menu
        edit_menu = self.menuBar().addMenu('&Edit')
        
        # Edit ToolBar
        edit_toolbar = QToolBar('Edit')
        edit_toolbar.setIconSize(QSize(60,60))
        self.addToolBar(Qt.BottomToolBarArea, edit_toolbar)

        # Undo and Redo Actions
        undo = self.create_action(self, './Icons/undo.png', 'Undo', 'Undoes the last edit', self.editor.undo)
        undo.setShortcut(QKeySequence.Undo)

        redo = self.create_action(self, './Icons/redo.png', 'Redo', 'Redoes the last edit', self.editor.redo)
        redo.setShortcut(QKeySequence.Redo)

        edit_menu.addActions([undo, redo])
        edit_toolbar.addActions([undo, redo])

        edit_menu.addSeparator
        edit_toolbar.addSeparator

        # Wrap Text
        wrapText_action = self.create_action(self, './Icons/wrap_text.png', 'Wrap Text', 'Wrap Text', self.toggle_wrap_text)
        wrapText_action.setShortcut('Ctrl+Shift+w')
        edit_menu.addAction(wrapText_action)
        edit_toolbar.addAction(wrapText_action)

        # Change text color
        ChooseColor = self.create_action(self, './Icons/ColorWheel.png', 'Set Text Color', 'Set Text Color', self.PickColor)
        ChooseColor.setShortcut('Ctrl+Shift+b')
        edit_menu.addAction(ChooseColor)
        edit_toolbar.addAction(ChooseColor)

        # Format Menu
        format_menu = self.menuBar().addMenu('&Format')

        # Format ToolBar
        format_toolbar = QToolBar('Format')
        format_toolbar.setIconSize(QSize(60,60))
        self.addToolBar(Qt.BottomToolBarArea, format_toolbar)

        # Bold, Italicisze, and Underline 
        boldText = self.create_action(self, './Icons/bold.png', 'Bold', 'Bold Text', 
                                      lambda x: self.editor.setFontWeight(QFont.Bold if x else QFont.Normal))
        boldText.setShortcut(QKeySequence.Bold)
        boldText.setCheckable(True)

        italicText = self.create_action(self, './Icons/italic.png', 'Italics', 'Italicize Text', self.editor.setFontItalic)
        italicText.setShortcut(QKeySequence.Italic)
        italicText.setCheckable(True)

        underlineText = self.create_action(self, './Icons/underline.png', 'Underline', 'Underline Text', self.editor.setFontUnderline)
        underlineText.setShortcut(QKeySequence.Underline)
        underlineText.setCheckable(True)

        format_menu.addActions([boldText, italicText, underlineText])
        format_toolbar.addActions([boldText, italicText, underlineText])

        format_menu.addSeparator
        format_toolbar.addSeparator


        self.update_title()

    # Function to wrap text
    def toggle_wrap_text(self):
        self.editor.setLineWrapMode(not self.editor.lineWrapMode())

    # Function to open a file
    def file_open(self):
        path, _ = QFileDialog.getOpenFileName(
            parent=self,
            caption='Open File',
            directory='',
            filter=self.filterTypes
        )

        # Try opening the file and copying all the data into
        # the editor for use. Else throw an exception. 
        if path:
            try:
                with open(path, 'r') as f:
                    text = f.read()
                    f.close()
            except Exception as e:
                self.dialog_message(str(e))
            else:
                self.path = path
                self.editor.setPlainText(text)
                self.update_title()

    # Function to save a file
    def file_save(self):
        # If this is a new file, go ahead and use the save_as method
        if self.path is None:
            self.file_saveAs()
        else:
            try:
                text = self.editor.toPlainText()
                with open(self.path, 'w') as f:
                    f.write(text)
                    f.close()
            except Exception as e:
                self.dialog_message(str(e))
    
    # Function to save file as 
    def file_saveAs(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            'Save File As',
            '',
            self.filterTypes
        )

        text = self.editor.toPlainText()

        # If we get an invalid path
        if not path:
            return
        # Else save the file if you can
        else:
            try:
                with open(path, 'w') as f:
                    f.write(text)
                    f.close()
            except Exception as e:
                self.dialog_message(str(e))
            else:   
                self.path = path
                self.update_title

    # Function to pick color
    def PickColor(self):
        self.c_color = None

        dlg = QColorDialog(self)
        if self.c_color:
            dlg.setCurrentColor(QColor(self.c_color))

        if dlg.exec_():
            self.setColor(dlg.currentColor().name())

    def setColor(self, color):
        if color != self.c_color:
            self.c_color = color

        # Until we switch to color palette, we have to do this
        if self.c_color:
            self.setStyleSheet("color: %s; background-color: black; selection-color: white; selection-background-color: blue;" %self.c_color)

        else:
            self.setStyleSheet("")

    def bold_text(self):
        formatted = QTextCharFormat()
        formatted.setFontWeight(self.boldText.isChecked() and QFont.Bold or QFont.Normal)
        self.mergeFormatOnWordOrSelection(formatted)

    # Update name
    def update_title(self):
        self.setWindowTitle('{0} - Void* Notepad'.format(os.path.basename(self.path) if self.path else 'New Note'))

    # This method is used to print exceptions/errors
    def dialog_message(self, message):
        dlg = QMessageBox(self)
        dlg.setTest(message)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()

    # This is how we create actions like open, save, and save as
    def create_action(self, parent, icon_path, action_name, set_status_tip, triggered_method):
        action = QAction(QIcon(icon_path), action_name, parent)
        action.setStatusTip(set_status_tip)
        action.triggered.connect(triggered_method)
        return action