# This is the main execution of our notepad 
# Checkout the similar files in John's branch 
# for more information on any of the files here. 

import os, sys
from PyQt5.QtWidgets import QApplication
import Notepad
import Folders

# Create a folder for this user 
# This part will be updated when my team implements the 
# ability to check on individual users 
new_folder = Folders.Folder("new_folder", None)
new_folder.add_note("TEST1")
new_folder.add_note("TEST2")

# Actually run the notepad 
app = QApplication(sys.argv)
screen = Notepad.Notepad()
screen.show()
sys.exit(app.exec_())
 