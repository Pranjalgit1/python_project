from tkinter import Tk, Button, Label
from file_operations import FileOperations
from duplicate_finder import DuplicateFinder
from duplicate_handler import DuplicateHandler
from config_manager import ConfigManager

class FileOrganizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Automatic File Organizer")
        self.config_manager = ConfigManager()
        self.file_ops = FileOperations(self.config_manager)
        self.duplicate_finder = DuplicateFinder()
        self.duplicate_handler = DuplicateHandler(root, self.duplicate_finder)
        self.setup_ui()
    
    def setup_ui(self):
        Button(self.root, text="Select Directory", 
               command=self.select_directory).pack(pady=20)
        Button(self.root, text="Organize Files", 
               command=self.organize_files).pack(pady=10) 
        Button(self.root, text="Undo", 
               command=self.undo).pack(pady=10)
        Button(self.root, text="Find Duplicates", 
               command=self.find_duplicates).pack(pady=10)
        Button(self.root, text="Custom Categories", 
               command=self.open_categories).pack(pady=10)
        self.status_label = Label(self.root, text="")
        self.status_label.pack()
    
    def select_directory(self):
        directory = self.file_ops.select_directory()
        if directory:
            self.status_label.config(text=f"Directory selected: {directory}")
            self.config_manager.load_config(directory)
    
    def organize_files(self):
        result = self.file_ops.organize_files()
        self.status_label.config(text=result)
    
    def undo(self):
        result = self.file_ops.undo()
        self.status_label.config(text=result)
    
    def find_duplicates(self):
        directory = self.file_ops.get_directory()
        if not directory:
            self.status_label.config(text="Please select a directory first.")
            return
        self.status_label.config(text="Scanning for duplicates...")
        self.root.update_idletasks()
        self.duplicate_handler.find_and_show_duplicates(directory, self.status_label)
    
    def open_categories(self):
        self.config_manager.open_categories_editor(
            self.root, 
            self.file_ops.get_directory()
        )

if __name__ == "__main__":
    root = Tk()
    app = FileOrganizer(root)
    root.mainloop()