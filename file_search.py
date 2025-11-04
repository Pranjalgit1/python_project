from tkinter import Toplevel, Frame, Label, Entry, Listbox, Button, Scrollbar
from tkinter import StringVar, END, BOTH, LEFT, RIGHT, Y, W, E
import os
import subprocess
import platform

class FileSearchWindow:
    
    def __init__(self, parent, directory):
        self.parent = parent
        self.directory = directory
        self.all_files = []
        self.window = Toplevel(parent)
        self.window.title("File Search & Open")
        self.window.geometry("700x500")
        self.scan_files()
        self.setup_ui()
    
    def scan_files(self):
        if not self.directory or not os.path.exists(self.directory):
            return
        for root_dir, _, files in os.walk(self.directory):
            for filename in files:
                file_path = os.path.join(root_dir, filename)
                rel_path = os.path.relpath(file_path, self.directory)
                self.all_files.append((filename, file_path, rel_path))
    
    def setup_ui(self):
    
        title_frame = Frame(self.window)
        title_frame.pack(pady=10, padx=10, fill='x')
        Label(title_frame, text="🔍 File Search & Open", 
              font=("Arial", 14, "bold")).pack()
        Label(title_frame, text=f"Searching in: {self.directory}", 
              font=("Arial", 9)).pack()
        Label(title_frame, text=f"Total files: {len(self.all_files)}", 
              font=("Arial", 9)).pack()
      
        search_frame = Frame(self.window)
        search_frame.pack(pady=10, padx=10, fill='x')
        Label(search_frame, text="Search:", font=("Arial", 10)).pack(side=LEFT, padx=5)
        self.search_var = StringVar()
        self.search_var.trace('w', self.on_search_change)
        
        search_entry = Entry(search_frame, textvariable=self.search_var, 
                            font=("Arial", 10), width=50)
        search_entry.pack(side=LEFT, fill='x', expand=True, padx=5)
        search_entry.focus()
        
        Button(search_frame, text="Clear", command=self.clear_search,
               font=("Arial", 9)).pack(side=LEFT, padx=5)
        
        results_frame = Frame(self.window)
        results_frame.pack(pady=5, padx=10, fill=BOTH, expand=True)
        
        Label(results_frame, text="Results:", font=("Arial", 10, "bold")).pack(anchor=W)
        
        list_frame = Frame(results_frame)
        list_frame.pack(fill=BOTH, expand=True)
        
        scrollbar = Scrollbar(list_frame)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        self.results_listbox = Listbox(list_frame, yscrollcommand=scrollbar.set,
                                       font=("Courier", 9), height=15)
        self.results_listbox.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.config(command=self.results_listbox.yview)
        
        self.results_listbox.bind('<Double-Button-1>', self.on_double_click)
        self.results_listbox.bind('<Return>', self.on_double_click)
        
       
        self.info_label = Label(self.window, text="Double-click or press Enter to open file", 
                               font=("Arial", 9), fg="gray")
        self.info_label.pack(pady=5)
        
        
        button_frame = Frame(self.window)
        button_frame.pack(pady=10, padx=10)
        
        Button(button_frame, text="Open Selected", command=self.open_selected,
               bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
               padx=15, pady=5).pack(side=LEFT, padx=5)
        Button(button_frame, text="Open Folder", command=self.open_folder,
               bg="#2196F3", fg="white", font=("Arial", 10, "bold"),
               padx=15, pady=5).pack(side=LEFT, padx=5)
        Button(button_frame, text="Close", command=self.window.destroy,
               bg="#9E9E9E", fg="white", font=("Arial", 10, "bold"),
               padx=15, pady=5).pack(side=LEFT, padx=5)
        
        self.update_results("")
    
    def on_search_change(self, *args):
        search_text = self.search_var.get()
        self.update_results(search_text)
    
    def update_results(self, search_text):
        self.results_listbox.delete(0, END)
        
        search_text = search_text.lower()
        matches = []
        for filename, file_path, rel_path in self.all_files:
            if search_text in filename.lower() or search_text in rel_path.lower():
                matches.append((filename, file_path, rel_path))
       
        for filename, file_path, rel_path in matches:
            display_text = f"{filename}  →  {rel_path}"
            self.results_listbox.insert(END, display_text)
        
        if search_text:
            self.info_label.config(text=f"Found {len(matches)} file(s) matching '{search_text}'")
        else:
            self.info_label.config(text=f"Showing all {len(matches)} files")
    
    def clear_search(self):
        self.search_var.set("")
    
    def get_selected_file(self):
        selection = self.results_listbox.curselection()
        if not selection:
            return None
        index = selection[0]
        search_text = self.search_var.get().lower()
        matches = []
        for filename, file_path, rel_path in self.all_files:
            if search_text in filename.lower() or search_text in rel_path.lower():
                matches.append(file_path)
        
        if index < len(matches):
            return matches[index]
        return None
    
    def on_double_click(self, event):
        self.open_selected()
    
    def open_selected(self):
        file_path = self.get_selected_file()
        if file_path:
            self.open_file(file_path)
    
    def open_file(self, file_path):
        try:
            if platform.system() == 'Windows':
                os.startfile(file_path)
            elif platform.system() == 'Darwin':  # macOS
                subprocess.run(['open', file_path])
            else:  # Linux
                subprocess.run(['xdg-open', file_path])
            
            self.info_label.config(text=f"Opened: {os.path.basename(file_path)}", fg="green")
        except Exception as e:
            self.info_label.config(text=f"Error opening file: {str(e)}", fg="red")
    
    def open_folder(self):
        file_path = self.get_selected_file()
        if file_path:
            folder_path = os.path.dirname(file_path)
            self.open_file(folder_path)
