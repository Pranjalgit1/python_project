from tkinter import Toplevel, Frame, Label, Button, Scrollbar, Text, END, WORD, BOTH, LEFT, RIGHT, Y
import os

class PreviewWindow:
    
    def __init__(self, parent, file_list, config_manager):
        self.parent = parent
        self.file_list = file_list  # List of (file_path, category) tuples
        self.config_manager = config_manager
        self.approved = False
        
        self.window = Toplevel(parent)
        self.window.title("Preview - Files to be Organized")
        self.window.geometry("700x500")
        
        self.setup_ui()
    
    def setup_ui(self):
        title_frame = Frame(self.window)
        title_frame.pack(pady=10, padx=10, fill='x')
        Label(title_frame, text="Files to be Organized", 
              font=("Arial", 14, "bold")).pack()
        Label(title_frame, text=f"Total files: {len(self.file_list)}", 
              font=("Arial", 10)).pack()
        list_frame = Frame(self.window)
        list_frame.pack(pady=10, padx=10, fill=BOTH, expand=True)
        scrollbar = Scrollbar(list_frame)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.text_widget = Text(list_frame, yscrollcommand=scrollbar.set, 
                                wrap=WORD, font=("Courier", 9))
        self.text_widget.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.config(command=self.text_widget.yview)
        self.populate_file_list()
        self.text_widget.config(state='disabled')
        button_frame = Frame(self.window)
        button_frame.pack(pady=10, padx=10)
        
        Button(button_frame, text="Proceed with Organization", 
               command=self.approve, bg="#4CAF50", fg="white",
               font=("Arial", 10, "bold"), padx=20, pady=5).pack(side=LEFT, padx=5)
        Button(button_frame, text="Cancel", 
               command=self.cancel, bg="#f44336", fg="white",
               font=("Arial", 10, "bold"), padx=20, pady=5).pack(side=LEFT, padx=5)
    
    def populate_file_list(self):
    
        self.text_widget.config(state='normal')

        category_files = {}
        for file_path, category in self.file_list:
            if category not in category_files:
                category_files[category] = []
            category_files[category].append(file_path)
        
        for category in sorted(category_files.keys()):
            files = category_files[category]
            self.text_widget.insert(END, f"\n📁 {category} ({len(files)} files)\n", "category")
            self.text_widget.insert(END, "─" * 60 + "\n")
            
            for file_path in files:
                filename = os.path.basename(file_path)
                file_size = self.get_file_size(file_path)
                self.text_widget.insert(END, f"  • {filename} ({file_size})\n")
            
            self.text_widget.insert(END, "\n")
        
        self.text_widget.tag_config("category", font=("Arial", 11, "bold"), 
                                    foreground="#2196F3")
        
        self.text_widget.config(state='disabled')
    
    def get_file_size(self, file_path):
        try:
            size = os.path.getsize(file_path)
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024.0:
                    return f"{size:.1f} {unit}"
                size /= 1024.0
            return f"{size:.1f} TB"
        except:
            return "Unknown"
    
    def approve(self):
        self.approved = True
        self.window.destroy()
    
    def cancel(self):
        self.approved = False
        self.window.destroy()
    
    def show(self):
        self.window.wait_window()
        return self.approved
