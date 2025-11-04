from tkinter import Tk, Button, Label, Frame, Menu
from file_operations import FileOperations
from duplicate_finder import DuplicateFinder
from duplicate_handler import DuplicateHandler
from config_manager import ConfigManager
from preview_window import PreviewWindow
from statistics_dashboard import StatisticsDashboard
from theme_manager import ThemeManager
from file_search import FileSearchWindow

class FileOrganizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Automatic File Organizer")
        self.root.geometry("500x550")
        
        self.config_manager = ConfigManager()
        self.file_ops = FileOperations(self.config_manager)
        self.duplicate_finder = DuplicateFinder()
        self.duplicate_handler = DuplicateHandler(root, self.duplicate_finder)
        self.theme_manager = ThemeManager()
        
        self.setup_menu()
        self.setup_ui()
        self.apply_theme()
    
    def setup_menu(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        
        # View menu
        view_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Statistics Dashboard", command=self.show_statistics)
        view_menu.add_command(label="File Search & Open", command=self.open_search)
        view_menu.add_separator()
        view_menu.add_command(label="Toggle Theme", command=self.toggle_theme)
    
    def setup_ui(self):
        # Title Frame
        title_frame = Frame(self.root)
        title_frame.pack(pady=20)
        
        title_label = Label(title_frame, text="📁 File Organizer", 
                           font=("Arial", 18, "bold"))
        title_label.pack()
        
        subtitle_label = Label(title_frame, text="Organize your files automatically", 
                              font=("Arial", 10))
        subtitle_label.pack()
        
   
        buttons_frame = Frame(self.root)
        buttons_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
      
        self.create_button(buttons_frame, "📂 Select Directory", 
                          self.select_directory, "#2196F3")
        self.create_button(buttons_frame, "🔍 Preview Files", 
                          self.preview_files, "#FF9800")
        self.create_button(buttons_frame, "✨ Organize Files", 
                          self.organize_files, "#4CAF50")
        self.create_button(buttons_frame, "↩️  Undo Organization", 
                          self.undo, "#9C27B0")
        self.create_button(buttons_frame, "🔎 Find Duplicates", 
                          self.find_duplicates, "#F44336")
        self.create_button(buttons_frame, "⚙️  Custom Categories", 
                          self.open_categories, "#607D8B")
        self.create_button(buttons_frame, "📊 Statistics Dashboard", 
                          self.show_statistics, "#00BCD4")
        self.create_button(buttons_frame, "🔍 Search Files", 
                          self.open_search, "#009688")
        
      
        status_frame = Frame(self.root)
        status_frame.pack(pady=10, padx=20, fill='x')
        self.status_label = Label(status_frame, text="Ready to organize files", 
                                 font=("Arial", 10), wraplength=450)
        self.status_label.pack()
        footer_frame = Frame(self.root)
        footer_frame.pack(side='bottom', pady=10)
        self.theme_label = Label(footer_frame, text=f"Theme: {self.theme_manager.get_current_theme().title()}", 
                              font=("Arial", 8))
        self.theme_label.pack()
    
    def create_button(self, parent, text, command, color):
   
        btn = Button(parent, text=text, command=command, 
                    bg=color, fg="white", font=("Arial", 11, "bold"),
                    padx=10, pady=8, relief="flat", cursor="hand2")
        btn.pack(pady=5, fill='x')
        return btn
    
    def select_directory(self):
        directory = self.file_ops.select_directory()
        if directory:
            self.status_label.config(text=f"✓ Directory selected: {directory}")
            self.config_manager.load_config(directory)
        else:
            self.status_label.config(text="Directory selection cancelled")
    
    def preview_files(self):
        directory = self.file_ops.get_directory()
        if not directory:
            self.status_label.config(text="⚠️  Please select a directory first.")
            return
        
        file_list = self.file_ops.get_file_preview_list()
        
        if not file_list:
            self.status_label.config(text="ℹ️  No files to organize in the selected directory.")
            return
        
        preview = PreviewWindow(self.root, file_list, self.config_manager)
        approved = preview.show()
        
        if approved:
            result = self.file_ops.organize_files()
            self.status_label.config(text=f"✓ {result}")
        else:
            self.status_label.config(text="Organization cancelled by user")
    
    def organize_files(self):
        result = self.file_ops.organize_files()
        self.status_label.config(text=f"✓ {result}")
    
    def undo(self):
        result = self.file_ops.undo()
        self.status_label.config(text=f"↩️  {result}")
    
    def find_duplicates(self):
        directory = self.file_ops.get_directory()
        if not directory:
            self.status_label.config(text="⚠️  Please select a directory first.")
            return
        self.status_label.config(text="🔎 Scanning for duplicates...")
        self.root.update_idletasks()
        self.duplicate_handler.find_and_show_duplicates(directory, self.status_label)
    
    def open_categories(self):
        self.config_manager.open_categories_editor(
            self.root, 
            self.file_ops.get_directory()
        )
    
    def show_statistics(self):
        directory = self.file_ops.get_directory()
        if not directory:
            self.status_label.config(text="⚠️  Please select a directory first.")
            return
        
        try:
            dashboard = StatisticsDashboard(self.root, directory, self.config_manager)
            self.status_label.config(text="📊 Statistics dashboard opened")
        except Exception as e:
            self.status_label.config(text=f"❌ Error opening dashboard: {str(e)}")
    
    def open_search(self):
        directory = self.file_ops.get_directory()
        if not directory:
            self.status_label.config(text="⚠️  Please select a directory first.")
            return
        
        try:
            search_window = FileSearchWindow(self.root, directory)
            self.status_label.config(text="🔍 File search opened")
        except Exception as e:
            self.status_label.config(text=f"❌ Error opening search: {str(e)}")
    
    def toggle_theme(self):
        new_theme = self.theme_manager.toggle_theme()
        self.apply_theme()
        self.status_label.config(text=f"🎨 Switched to {new_theme} theme")
        self.theme_label.config(text=f"Theme: {new_theme.title()}")
    
    def apply_theme(self):
        self.theme_manager.apply_theme_to_window(self.root)

if __name__ == "__main__":
    root = Tk()
    app = FileOrganizer(root)
    root.mainloop()