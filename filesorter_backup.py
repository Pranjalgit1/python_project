import os
import shutil
import hashlib
import json
import time
from tkinter import *
from tkinter import filedialog, messagebox, simpledialog
from tkinter import ttk
from send2trash import send2trash

class FileOrganizer:
    """
    A GUI application to organize files into categories, find duplicates, and manage file organization.
    """
    
    def __init__(self, root):
        """Initialize the File Organizer application with all necessary variables and UI components."""
        self.root = root
        self.root.title("Automatic File Organizer")
        
        # Core variables for file organization
        self.directory = None  # The folder selected by the user to organize
        self.undo_data = []  # Tracks file moves so we can undo them later
        self.config = self.load_config()  # Load file categorization rules from config.json
        
        # Variables for duplicate file detection
        self.hash_to_paths = {}  # Maps file content hashes to file paths
        self.duplicate_groups = []  # Groups of files with identical content
        self.current_group_index = 0  # Which duplicate group we're currently reviewing
        self.log_path = None  # Where we save the duplicate review log

        # Create the main UI buttons
        select_button = Button(root, text="Select Directory", command=self.select_directory) 
        select_button.pack(pady=20)  # Add 20 pixels of vertical spacing

        organize_button = Button(root, text="Organize Files", command=self.organize_files)
        organize_button.pack(pady=10)

        undo_button = Button(root, text="Undo", command=self.undo)
        undo_button.pack(pady=10)

        duplicates_button = Button(root, text="Find Duplicates", command=self.find_duplicates_workflow)
        duplicates_button.pack(pady=10)

        

        categories_button = Button(root, text="Custom Categories", command=self.open_categories_editor)
        categories_button.pack(pady=10)

        self.status_label = Label(root, text="")
        self.status_label.pack()

    def select_directory(self):
        self.directory = filedialog.askdirectory() #User selects a folder and the path is stored in self.directory
        if self.directory:
            self.status_label.config(text="Directory selected: " + self.directory)
            # Reload config with per-directory override if present
            self.config = self.load_config(self.directory)

    def organize_files(self):
        if self.directory:
            self.undo_data = []
            for filename in os.listdir(self.directory):
                file_path = os.path.join(self.directory, filename)
                if os.path.isfile(file_path):
                    file_extension = os.path.splitext(filename)[1]
                    category = self.ext_to_category(file_extension, self.config)
                    destination = os.path.join(self.directory, category)
                    if not os.path.exists(destination):
                        os.makedirs(destination)
                    self.undo_data.append((file_path, destination))
                    shutil.move(file_path, destination)
            self.status_label.config(text="Files organized successfully!")
        else:
            self.status_label.config(text="Please select a directory first.")

   
    def default_config(self):
        return {"categories": {}, "default_folder": "Others"}

    def app_config_path(self):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')

    def dir_config_path(self, directory):
        return os.path.join(directory, '.organizer_config.json')

    def normalize_extension(self, ext):
        if not ext:
            return ''
        ext = str(ext).strip().lower()
        if not ext.startswith('.'):
            ext = '.' + ext
        return ext

    def sanitize_folder_name(self, name):
        invalid = '<>:"/\\|?*'
        safe = ''.join(ch for ch in str(name) if ch not in invalid).strip()
        return safe or 'Folder'

    def normalize_config(self, cfg):
        if not isinstance(cfg, dict):
            return self.default_config()
        categories = cfg.get('categories') or {}
        default_folder = cfg.get('default_folder') or 'Others'
        norm = {"categories": {}, "default_folder": self.sanitize_folder_name(default_folder)}
        for folder, exts in categories.items():
            safe_folder = self.sanitize_folder_name(folder)
            if not isinstance(exts, list):
                continue
            norm_exts = []
            for e in exts:
                ne = self.normalize_extension(e)
                if ne and ne not in norm_exts:
                    norm_exts.append(ne)
            if norm_exts:
                norm["categories"][safe_folder] = norm_exts
        return norm

    def load_config(self, directory=None):
     
        if directory:
            p = self.dir_config_path(directory)
            try:
                if os.path.exists(p):
                    with open(p, 'r', encoding='utf-8') as f:
                        return self.normalize_config(json.load(f))
            except Exception:
                self.append_log({"timestamp": time.time(), "action": "config_load_error", "scope": "dir", "path": p})
                return self.default_config()
       
        p = self.app_config_path()
        try:
            if os.path.exists(p):
                with open(p, 'r', encoding='utf-8') as f:
                    return self.normalize_config(json.load(f))
        except Exception:
            self.append_log({"timestamp": time.time(), "action": "config_load_error", "scope": "app", "path": p})
            return self.default_config()
        return self.default_config()

    def save_config(self, config, directory=None):
        cfg = self.normalize_config(config)
        target = self.dir_config_path(directory) if directory else self.app_config_path()
  
        try:
            if os.path.exists(target):
                shutil.copy2(target, target + '.bak')
        except Exception:
            pass
        with open(target, 'w', encoding='utf-8') as f:
            json.dump(cfg, f, indent=2)
        self.append_log({"timestamp": time.time(), "action": "config_saved", "target": target})
        return cfg

    def ext_to_category(self, ext, config):
        ext = self.normalize_extension(ext)
        for folder, exts in config.get('categories', {}).items():
            if ext in exts:
                return folder
        return config.get('default_folder', 'Others')


    def open_categories_editor(self):
        cfg = json.loads(json.dumps(self.config)) 
        win = Toplevel(self.root)
        win.title("Custom Categories")
        win.geometry("700x420")

        left = Frame(win)
        left.pack(side=LEFT, fill=Y, padx=10, pady=10)
        right = Frame(win)
        right.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)

        Label(left, text="Categories").pack(anchor=W)
        cat_list = Listbox(left, height=18)
        cat_list.pack(fill=Y)

        def refresh_list():
            cat_list.delete(0, END)
            for folder in sorted(cfg['categories'].keys()):
                cat_list.insert(END, folder)

        Label(right, text="Default Folder").pack(anchor=W)
        default_var = StringVar(value=cfg.get('default_folder', 'Others'))
        Entry(right, textvariable=default_var).pack(fill=X)

        Label(right, text="Extensions (comma-separated)").pack(anchor=W, pady=(10, 0))
        exts_var = StringVar(value="")
        exts_entry = Entry(right, textvariable=exts_var)
        exts_entry.pack(fill=X)

        msg_var = StringVar(value="")
        msg = Label(right, textvariable=msg_var, fg="red")
        msg.pack(anchor=W, pady=(6, 0))

        def on_select(event=None):
            sel = cat_list.curselection()
            if not sel:
                exts_var.set("")
                return
            folder = cat_list.get(sel[0])
            exts_var.set(", ".join(cfg['categories'].get(folder, [])))

        cat_list.bind('<<ListboxSelect>>', on_select)

        def add_category():
            name = simpledialog.askstring("Add Category", "Folder name:")
            if not name:
                return
            safe = self.sanitize_folder_name(name)
            if safe in cfg['categories']:
                msg_var.set("Category already exists")
                return
            cfg['categories'][safe] = []
            refresh_list()

        def delete_category():
            sel = cat_list.curselection()
            if not sel:
                return
            folder = cat_list.get(sel[0])
            if folder == cfg.get('default_folder'):
                msg_var.set("Cannot delete default folder")
                return
            del cfg['categories'][folder]
            refresh_list()
            exts_var.set("")

        def save_close():
            # Apply edits to selected folder
            sel = cat_list.curselection()
            if sel:
                folder = cat_list.get(sel[0])
                raw = exts_var.get()
                parts = [p.strip() for p in raw.split(',') if p.strip()]
                norm = []
                for p in parts:
                    e = self.normalize_extension(p)
                    if e and e not in norm:
                        norm.append(e)
                cfg['categories'][folder] = norm
            cfg['default_folder'] = self.sanitize_folder_name(default_var.get() or 'Others')
           
            seen = {}
            for folder, exts in cfg['categories'].items():
                for e in exts:
                    if e in seen and seen[e] != folder:
                        msg_var.set(f"Duplicate ext {e} in {seen[e]} and {folder}")
                        return
                    seen[e] = folder
            # Save to per-directory if selected; else app-level
            target_dir = self.directory if self.directory else None
            self.config = self.save_config(cfg, directory=target_dir)
            win.destroy()

        Button(left, text="Add Category", command=add_category).pack(fill=X, pady=(8, 2))
        Button(left, text="Delete Category", command=delete_category).pack(fill=X)
        Button(right, text="Save & Close", command=save_close).pack(anchor=E, pady=(12, 0))
        Button(right, text="Cancel", command=win.destroy).pack(anchor=E)

        refresh_list()

    def compute_file_hash(self, file_path, chunk_size=1024 * 1024):
        hasher = hashlib.sha256()
        try:
            with open(file_path, 'rb') as f:
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception:
            return None

    def scan_directory_hashes(self):
        self.hash_to_paths = {}
        if not self.directory:
            return
        for root_dir, _, files in os.walk(self.directory):
            for name in files:
                file_path = os.path.join(root_dir, name)
                if not os.path.isfile(file_path):
                    continue
                file_hash = self.compute_file_hash(file_path)
                if not file_hash:
                    continue
                self.hash_to_paths.setdefault(file_hash, []).append(file_path)
        self.duplicate_groups = [paths for paths in self.hash_to_paths.values() if len(paths) > 1]

    def find_duplicates_workflow(self):
        if not self.directory:
            self.status_label.config(text="Please select a directory first.")
            return
        self.status_label.config(text="Scanning for duplicates...")
        self.root.update_idletasks()
        self.scan_directory_hashes()
        if not self.duplicate_groups:
            messagebox.showinfo("Duplicates", "No duplicates found.")
            self.status_label.config(text="No duplicates found.")
            return
        self.current_group_index = 0
        self.log_path = os.path.join(self.directory, 'duplicates_log.json')
        self.open_duplicates_window()

    def open_duplicates_window(self):
        window = Toplevel(self.root)
        window.title("Duplicate Files Review")
        window.geometry("800x500")

        header_frame = Frame(window)
        header_frame.pack(fill=X, padx=10, pady=10)

        self.group_label_var = StringVar()
        group_label = Label(header_frame, textvariable=self.group_label_var, font=("Arial", 12, "bold"))
        group_label.pack(side=LEFT)

        controls_frame = Frame(window)
        controls_frame.pack(fill=X, padx=10, pady=(0, 10))

        self.check_vars = []

        list_frame = Frame(window)
        list_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        columns = ("#", "Path")
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        self.tree.heading("#", text="#")
        self.tree.heading("Path", text="Path")
        self.tree.column("#", width=40, anchor=CENTER)
        self.tree.column("Path", width=700, anchor=W)
        self.tree.pack(fill=BOTH, expand=True, side=LEFT)

        scrollbar = Scrollbar(list_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)

        actions_frame = Frame(window)
        actions_frame.pack(fill=X, padx=10, pady=10)

        delete_btn = Button(actions_frame, text="Delete Selected (Recycle Bin)", command=self.delete_selected)
        delete_btn.pack(side=LEFT, padx=5)

        move_btn = Button(actions_frame, text="Move Selected...", command=self.move_selected)
        move_btn.pack(side=LEFT, padx=5)

        keep_btn = Button(actions_frame, text="Keep Both (Skip)", command=self.keep_both)
        keep_btn.pack(side=LEFT, padx=5)

        select_all_but_one_btn = Button(actions_frame, text="Select All But First", command=self.select_all_but_first)
        select_all_but_one_btn.pack(side=LEFT, padx=5)

        nav_frame = Frame(window)
        nav_frame.pack(fill=X, padx=10, pady=10)

        prev_btn = Button(nav_frame, text="Previous", command=self.prev_group)
        prev_btn.pack(side=LEFT)

        next_btn = Button(nav_frame, text="Next", command=self.next_group)
        next_btn.pack(side=RIGHT)

        self.dup_window = window
        self.refresh_group_view()

    def refresh_group_view(self):
        total = len(self.duplicate_groups)
        idx = self.current_group_index + 1
        self.group_label_var.set(f"Group {idx} of {total} (same content)")
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.check_vars = []
        current_paths = self.duplicate_groups[self.current_group_index]
        for i, path in enumerate(current_paths, start=1):
            self.tree.insert('', END, values=(i, path))

    def get_selected_paths(self):
        selected = []
        for item in self.tree.selection():
            vals = self.tree.item(item, 'values')
            if len(vals) >= 2:
                selected.append(vals[1])
        return selected

    def select_all_but_first(self):
       
        self.tree.selection_remove(self.tree.selection())
        items = self.tree.get_children()
        for item in items[1:]:
            self.tree.selection_add(item)

    def prev_group(self):
        if self.current_group_index > 0:
            self.current_group_index -= 1
            self.refresh_group_view()

    def next_group(self):
        if self.current_group_index < len(self.duplicate_groups) - 1:
            self.current_group_index += 1
            self.refresh_group_view()
        else:
            messagebox.showinfo("Review", "Reached last group.")

    def append_log(self, entry):
        data = []
        if self.log_path and os.path.exists(self.log_path):
            try:
                with open(self.log_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except Exception:
                data = []
        data.append(entry)
        try:
            with open(self.log_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass

    def delete_selected(self):
        current_paths = list(self.duplicate_groups[self.current_group_index])
        selected = self.get_selected_paths()
        if not selected:
            messagebox.showwarning("Delete", "No files selected.")
            return

        deleted = []
        missing = []
        errors = []

        def normalize_path(p):
          
            if not p:
                return p
            p = str(p)
            if p.startswith('\\\\?\\'):
                p = p[4:]
            return os.path.abspath(os.path.normpath(p))

        for raw_path in selected:
            path = normalize_path(raw_path)
            try:
                if not os.path.exists(path):
                    missing.append(path)
                    continue
                try:
                    send2trash(path)
                    deleted.append(path)
                except Exception as e_send:
                  
                    errors.append((path, f"send2trash error: {e_send}"))
                    try:
                        fallback_dir = os.path.join(self.directory, "Duplicates_Trash")
                        os.makedirs(fallback_dir, exist_ok=True)
                        dest = os.path.join(fallback_dir, os.path.basename(path))
                        i = 1
                        base, ext = os.path.splitext(dest)
                        while os.path.exists(dest):
                            dest = f"{base}({i}){ext}"
                            i += 1
                        shutil.move(path, dest)
                        deleted.append(path)  
                    except Exception as e_move:
                        errors.append((path, f"fallback move error: {e_move}"))
            except Exception as e:
                errors.append((raw_path, str(e)))

        # Append detailed log entry
        self.append_log({
            "timestamp": time.time(),
            "group_index": self.current_group_index,
            "action": "delete",
            "selected_raw": selected,
            "deleted": deleted,
            "missing": missing,
            "errors": errors,
            "group": current_paths
        })

        if errors:
            err_text = "\n".join([f"{p}: {msg}" for p, msg in errors])
            messagebox.showerror("Delete Error", f"Some files could not be moved to Recycle Bin or fallback:\n{err_text}")

      
        remaining = [p for p in current_paths if p not in deleted and p not in missing]
        self.duplicate_groups[self.current_group_index] = remaining
        if len(remaining) <= 1:
            try:
                del self.duplicate_groups[self.current_group_index]
            except IndexError:
                pass
            if self.current_group_index >= len(self.duplicate_groups):
                self.current_group_index = max(0, len(self.duplicate_groups) - 1)

        if not self.duplicate_groups:
            messagebox.showinfo("Duplicates", "No more duplicate groups.")
            try:
                self.dup_window.destroy()
            except Exception:
                pass
            self.status_label.config(text="Duplicates processed.")
            return

        self.refresh_group_view()


    def move_selected(self):
        current_paths = list(self.duplicate_groups[self.current_group_index])
        selected = self.get_selected_paths()
        if not selected:
            messagebox.showwarning("Move", "No files selected.")
            return
        target_dir = filedialog.askdirectory(title="Select target directory")
        if not target_dir:
            return
        for path in selected:
            try:
                filename = os.path.basename(path)
                dest = os.path.join(target_dir, filename)
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir)
                shutil.move(path, dest)
            except Exception as e:
                messagebox.showerror("Move Error", f"Failed to move {path}: {e}")
        self.append_log({
            "timestamp": time.time(),
            "group_index": self.current_group_index,
            "action": "move",
            "target": target_dir,
            "selected": selected,
            "group": current_paths
        })
        remaining = [p for p in current_paths if p not in selected]
        self.duplicate_groups[self.current_group_index] = remaining
        if len(remaining) <= 1:
            del self.duplicate_groups[self.current_group_index]
            if self.current_group_index >= len(self.duplicate_groups):
                self.current_group_index = max(0, len(self.duplicate_groups) - 1)
        if not self.duplicate_groups:
            messagebox.showinfo("Duplicates", "No more duplicate groups.")
            self.dup_window.destroy()
            self.status_label.config(text="Duplicates processed.")
            return
        self.refresh_group_view()

    def keep_both(self):
        current_paths = list(self.duplicate_groups[self.current_group_index])
        self.append_log({
            "timestamp": time.time(),
            "group_index": self.current_group_index,
            "action": "skip",
            "group": current_paths
        })
        # Advance to next group without changes
        if self.current_group_index < len(self.duplicate_groups) - 1:
            self.current_group_index += 1
            self.refresh_group_view()
        else:
            messagebox.showinfo("Review", "Review complete.")
            self.dup_window.destroy()
            self.status_label.config(text="Duplicates processed.")

    def undo(self):
        if self.undo_data:
            for file_path, destination in self.undo_data:
                filename = os.path.basename(file_path)
                shutil.move(os.path.join(destination, filename), self.directory)
            self.undo_data = []
            self.status_label.config(text="Files restored to original state.")
        else:
            self.status_label.config(text="Nothing to undo.")

if __name__ == "__main__":
    root = Tk()
    app = FileOrganizer(root)
    root.mainloop()