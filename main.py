from tkinter import Tk, Button, Label, Frame, Menu
from file_operations import FileOperations
from duplicate_finder import DuplicateFinder
from duplicate_handler import DuplicateHandler
from config_manager import ConfigManager
from preview_window import PreviewWindow
from statistics_dashboard import StatisticsDashboard
from theme_manager import ThemeManager
from file_search import FileSearchWindow
from login_window import LoginWindow

class FileOrganizer:
    def __init__(self, root, current_user):
        self.root = root
        self.root.title("Automatic File Organizer")
        self.root.geometry("580x650")
        self.current_user = current_user
        
        # Set window background color
        self.root.configure(bg="#FAFAFA")
        
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
        
        # File menu
        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.root.quit)
    
    def setup_ui(self):
        # Purple Header Frame
        header_frame = Frame(self.root, bg="#673AB7", height=140)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Title in header
        title_label = Label(header_frame, text="📁 File Organizer", 
                           font=("Segoe UI", 22, "bold"), bg="#673AB7", fg="white")
        title_label.pack(pady=(25, 5))
        
        # Subtitle in header
        subtitle_label = Label(header_frame, text="Organize your files automatically", 
                              font=("Segoe UI", 11), bg="#673AB7", fg="white")
        subtitle_label.pack(pady=(0, 5))
        
        # User info in header
        user_label = Label(header_frame, text=f"👤 {self.current_user}", 
                          font=("Segoe UI", 10), bg="#673AB7", fg="#E1BEE7")
        user_label.pack(pady=2)
        
        # Main content frame with light background
        content_frame = Frame(self.root, bg="#FAFAFA")
        content_frame.pack(fill='both', expand=True, padx=25, pady=20)
        
        # Buttons container
        buttons_frame = Frame(content_frame, bg="#FAFAFA")
        buttons_frame.pack(fill='both', expand=True)
        
        self.create_modern_button(buttons_frame, "📂 Select Directory", 
                          self.select_directory, "#2196F3", "#1976D2")
        self.create_modern_button(buttons_frame, "⚙️  File Operations", 
                          self.open_file_operations, "#FF9800", "#F57C00")
        self.create_modern_button(buttons_frame, "✨ Organize Files", 
                          self.organize_files, "#4CAF50", "#388E3C")
        self.create_modern_button(buttons_frame, "↩️  Undo Organization", 
                          self.undo, "#9C27B0", "#7B1FA2")
        self.create_modern_button(buttons_frame, "🔍 Search Files", 
                          self.open_search, "#009688", "#00796B")
        
        # Status bar with green background
        status_frame = Frame(self.root, bg="#E8F5E9", height=50)
        status_frame.pack(fill='x', side='bottom')
        status_frame.pack_propagate(False)
        
        self.status_label = Label(status_frame, text="Ready to organize files", 
                                 font=("Segoe UI", 10), wraplength=520, 
                                 bg="#E8F5E9", fg="#2E7D32")
        self.status_label.pack(pady=15)
    
    def create_modern_button(self, parent, text, command, color, hover_color):
        """Create a modern styled button with hover effect"""
        btn = Button(parent, text=text, command=command, 
                    bg=color, fg="white", font=("Segoe UI", 13, "bold"),
                    padx=20, pady=15, relief="flat", cursor="hand2",
                    activebackground=hover_color, activeforeground="white",
                    borderwidth=0, highlightthickness=0)
        btn.pack(pady=8, fill='x')
        
        # Bind hover effects
        def on_enter(e):
            btn['background'] = hover_color
            btn.configure(relief="raised", bd=2)
        
        def on_leave(e):
            btn['background'] = color
            btn.configure(relief="flat", bd=0)
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn
    
    def create_button(self, parent, text, command, color):
        """Legacy button method for compatibility"""
        btn = Button(parent, text=text, command=command, 
                    bg=color, fg="white", font=("Segoe UI", 11, "bold"),
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
    
    def open_file_operations(self):
        """Open File Operations window with multiple options"""
        from tkinter import Toplevel
        
        # Check if directory is selected
        directory = self.file_ops.get_directory()
        if not directory:
            self.status_label.config(text="⚠️  Please select a directory first.")
            return
        
        # Create File Operations window
        ops_window = Toplevel(self.root)
        ops_window.title("File Operations")
        ops_window.geometry("450x550")
        ops_window.resizable(False, False)
        ops_window.configure(bg="#f5f5f5")
        
        # Center the window
        ops_window.update_idletasks()
        x = (ops_window.winfo_screenwidth() // 2) - (ops_window.winfo_width() // 2)
        y = (ops_window.winfo_screenheight() // 2) - (ops_window.winfo_height() // 2)
        ops_window.geometry(f"+{x}+{y}")
        
        # Header
        header = Frame(ops_window, bg="#673AB7", height=100)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        Label(header, text="🛠️  File Operations", 
              font=("Segoe UI", 18, "bold"), bg="#673AB7", fg="white").pack(pady=15)
        
        Label(header, text=f"📁 {directory}", 
              font=("Segoe UI", 9), fg="#E1BEE7", bg="#673AB7",
              wraplength=400).pack(pady=5)
        
        # Buttons frame
        btn_frame = Frame(ops_window, bg="#f5f5f5")
        btn_frame.pack(pady=30, padx=30, fill='both', expand=True)
        
        # Create modern buttons
        def create_ops_button(text, command, color, hover):
            btn = Button(btn_frame, text=text, 
                   command=lambda: [command(), ops_window.destroy()],
                   bg=color, fg="white", font=("Segoe UI", 12, "bold"),
                   padx=25, pady=14, relief="flat", cursor="hand2",
                   activebackground=hover, borderwidth=0)
            btn.pack(pady=8, fill='x')
            
            def on_enter(e):
                btn['background'] = hover
            def on_leave(e):
                btn['background'] = color
            
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
            return btn
        
        # Preview Files button
        create_ops_button("🔍 Preview Files", self.preview_files, "#FF9800", "#F57C00")
        
        # Find Duplicates button
        create_ops_button("🔎 Find Duplicates", self.find_duplicates, "#F44336", "#D32F2F")
        
        # Custom Categories button
        create_ops_button("⚙️  Custom Categories", self.open_categories, "#607D8B", "#455A64")
        
        # Statistics Dashboard button
        create_ops_button("📊 Statistics Dashboard", self.show_statistics, "#00BCD4", "#0097A7")
        
        # Close button
        close_btn = Button(btn_frame, text="✕ Close", 
               command=ops_window.destroy,
               bg="#9E9E9E", fg="white", font=("Segoe UI", 11, "bold"),
               padx=20, pady=10, relief="flat", cursor="hand2")
        close_btn.pack(pady=15, fill='x')
        
        def close_hover_in(e):
            close_btn['background'] = "#757575"
        def close_hover_out(e):
            close_btn['background'] = "#9E9E9E"
        
        close_btn.bind("<Enter>", close_hover_in)
        close_btn.bind("<Leave>", close_hover_out)
    
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
        # Theme toggle disabled - using fixed colorful Material Design
        self.status_label.config(text="🎨 Using Modern Material Design Theme")
    
    def apply_theme(self):
        # Theme is now fixed to colorful Material Design
        # Theme manager disabled for consistent colorful UI
        pass

if __name__ == "__main__":
    # Show login window first
    login = LoginWindow()
    authenticated, username = login.show()
    
    if authenticated:
        # Create and show main application
        root = Tk()
        app = FileOrganizer(root, username)
        root.mainloop()
    else:
        # User cancelled login
        print("Login cancelled")