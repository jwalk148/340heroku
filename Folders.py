# See Folders.py in John's branch for more information 

class Folder:
    def __init__(self, name, notes): 
        self.name = name
        self.notes = []

    def add_note(self, note_title):
        self.notes.append(note_title)

    