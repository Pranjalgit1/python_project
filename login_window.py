from tkinter import Tk, Label, Entry, Button, StringVar, Frame
import json
import os

class LoginWindow:
    """Simple login window for admin authentication"""
    
    def __init__(self):
        self.authenticated = False
        self.username = None
        
        self.root = Tk()
        self.root.title("File Organizer - Login")
        self.root.geometry("500x500")
        self.root.resizable(False, False)
        self.root.configure(bg="#f5f5f5")
        
        # Center the window
        self.center_window()
        
        # Load credentials
        self.credentials = self.load_credentials()
        
        self.setup_ui()
    
    def load_credentials(self):
        """Load credentials from JSON file"""
        cred_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'credentials.json')
        try:
            with open(cred_file, 'r') as f:
                return json.load(f)
        except:
            # Default credentials if file doesn't exist
            return {"admin": "admin"}
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_ui(self):
        """Create the login UI"""
        # Header with gradient-like effect
        header = Frame(self.root, bg="#3f51b5", height=130)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        Label(header, text="🔐", font=("Segoe UI", 40), bg="#3f51b5").pack(pady=(10,5))
        Label(header, text="File Organizer", 
              font=("Segoe UI", 22, "bold"), bg="#3f51b5", fg="white").pack()
        Label(header, text="Secure Login", 
              font=("Segoe UI", 10), bg="#3f51b5", fg="#E8EAF6").pack(pady=(3,10))
        
        # Main form frame
        form_frame = Frame(self.root, bg="#f5f5f5")
        form_frame.pack(pady=30, padx=50, fill='both', expand=True)
        
        # Username
        Label(form_frame, text="Username", 
              font=("Segoe UI", 10, "bold"), bg="#f5f5f5", fg="#424242").pack(anchor='w', pady=(10,5))
        self.username_var = StringVar()
        username_entry = Entry(form_frame, textvariable=self.username_var,
                              font=("Segoe UI", 12), relief="solid", bd=1,
                              highlightthickness=2, highlightcolor="#3f51b5")
        username_entry.pack(fill='x', ipady=8)
        username_entry.focus()
        
        # Password
        Label(form_frame, text="Password", 
              font=("Segoe UI", 10, "bold"), bg="#f5f5f5", fg="#424242").pack(anchor='w', pady=(20,5))
        self.password_var = StringVar()
        password_entry = Entry(form_frame, textvariable=self.password_var,
                              font=("Segoe UI", 12), show="●", relief="solid", bd=1,
                              highlightthickness=2, highlightcolor="#3f51b5")
        password_entry.pack(fill='x', ipady=8)
        
        # Bind Enter key to login
        username_entry.bind('<Return>', lambda e: password_entry.focus())
        password_entry.bind('<Return>', lambda e: self.attempt_login())
        
        # Status Label
        self.status_label = Label(form_frame, text="", 
                                 font=("Segoe UI", 9), bg="#f5f5f5")
        self.status_label.pack(pady=10)
        
        # Buttons
        login_btn = Button(form_frame, text="Login", command=self.attempt_login,
               bg="#4CAF50", fg="white", font=("Segoe UI", 13, "bold"),
               padx=50, pady=14, cursor="hand2", relief="flat", 
               activebackground="#388E3C", borderwidth=0)
        login_btn.pack(pady=(20,10), fill='x')
        
        # Hover effect for login button
        def login_hover_in(e):
            login_btn['background'] = "#388E3C"
        def login_hover_out(e):
            login_btn['background'] = "#4CAF50"
        login_btn.bind("<Enter>", login_hover_in)
        login_btn.bind("<Leave>", login_hover_out)
        
        exit_btn = Button(form_frame, text="Exit", command=self.exit_application,
               bg="#757575", fg="white", font=("Segoe UI", 11, "bold"),
               padx=40, pady=10, cursor="hand2", relief="flat",
               activebackground="#616161", borderwidth=0)
        exit_btn.pack(fill='x')
        
        # Hover effect for exit button
        def exit_hover_in(e):
            exit_btn['background'] = "#616161"
        def exit_hover_out(e):
            exit_btn['background'] = "#757575"
        exit_btn.bind("<Enter>", exit_hover_in)
        exit_btn.bind("<Leave>", exit_hover_out)
    
    def attempt_login(self):
        """Attempt to login with provided credentials"""
        username = self.username_var.get().strip()
        password = self.password_var.get()
        
        if not username or not password:
            self.status_label.config(text="Please enter both username and password", fg="red")
            return
        
        # Simple authentication - check if username exists and password matches
        if username in self.credentials and self.credentials[username] == password:
            self.authenticated = True
            self.username = username
            self.status_label.config(text="Login successful!", fg="green")
            self.root.after(500, self.root.quit)  # Close after 0.5 seconds
        else:
            self.status_label.config(text="Invalid username or password", fg="red")
            self.password_var.set("")  # Clear password field
            self.password_entry.focus()
    
    def exit_application(self):
        """Exit the entire application"""
        self.authenticated = False
        self.root.quit()
    
    def show(self):
        """Show the login window and wait for authentication"""
        self.root.mainloop()
        self.root.destroy()
        return self.authenticated, self.username
