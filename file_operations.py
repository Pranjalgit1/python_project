import os
import shutil
from tkinter import filedialog

class FileOperations:
  
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.directory = None
        self.undo_data = []
    
    def select_directory(self):
        self.directory = filedialog.askdirectory()
        return self.directory
    
    def get_directory(self):
  
        return self.directory
    
    def organize_files(self):
  
        if not self.directory:
            return "Please select a directory first."
        
        self.undo_data = []
        config = self.config_manager.get_config()
        
        for filename in os.listdir(self.directory):
            file_path = os.path.join(self.directory, filename)
            
            if os.path.isfile(file_path):
                file_extension = os.path.splitext(filename)[1]
                category = self.config_manager.ext_to_category(file_extension)
                destination = os.path.join(self.directory, category)
                
                if not os.path.exists(destination):
                    os.makedirs(destination)
                
                self.undo_data.append((file_path, destination))
                shutil.move(file_path, destination)
        
        return "Files organized successfully!"
    
    def undo(self):
        if not self.undo_data:
            return "Nothing to undo."
        
        for file_path, destination in self.undo_data:
            filename = os.path.basename(file_path)
            shutil.move(os.path.join(destination, filename), self.directory)
        
        self.undo_data = []
        return "Files restored to original state."