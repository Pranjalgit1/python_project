import os
import json
import time
import shutil
from tkinter import Toplevel, Frame, Button, Label, StringVar, Scrollbar, CENTER, W
from tkinter import LEFT, RIGHT, X, Y, BOTH, END, filedialog, messagebox
from tkinter import ttk
from send2trash import send2trash

class DuplicateHandler:
    
    def __init__(self, root, duplicate_finder):
        self.root = root
        self.duplicate_finder = duplicate_finder
        self.current_group_index = 0
        self.log_path = None
        self.directory = None
        self.dup_window = None
    
    def find_and_show_duplicates(self, directory, status_label):
        self.directory = directory
        duplicate_groups = self.duplicate_finder.scan_directory(directory)
        
        if not duplicate_groups:
            messagebox.showinfo("Duplicates", "No duplicates found.")
            status_label.config(text="No duplicates found.")
            return
        
        self.current_group_index = 0
        self.log_path = os.path.join(directory, 'duplicates_log.json')
        self.open_duplicates_window()
    
    def open_duplicates_window(self):
        """Create duplicate review window"""
        window = Toplevel(self.root)
        window.title("Duplicate Files Review")
        window.geometry("800x500")
        
 
        header_frame = Frame(window)
        header_frame.pack(fill=X, padx=10, pady=10)
        
        self.group_label_var = StringVar()
        Label(header_frame, textvariable=self.group_label_var, 
              font=("Arial", 12, "bold")).pack(side=LEFT)
        
  
        list_frame = Frame(window)
        list_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        columns = ("#", "Path")
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        self.tree.heading("#", text="#")
        self.tree.heading("Path", text="Path")
        self.tree.column("#", width=40, anchor=CENTER)
        self.tree.column("Path", width=700, anchor=W)
        self.tree.pack(fill=BOTH, expand=True, side=LEFT)
        
        scrollbar = Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        actions_frame = Frame(window)
        actions_frame.pack(fill=X, padx=10, pady=10)
        
        Button(actions_frame, text="Delete Selected (Recycle Bin)", 
               command=self.delete_selected).pack(side=LEFT, padx=5)
        Button(actions_frame, text="Move Selected...", 
               command=self.move_selected).pack(side=LEFT, padx=5)
        Button(actions_frame, text="Keep Both (Skip)", 
               command=self.keep_both).pack(side=LEFT, padx=5)
        Button(actions_frame, text="Select All But First", 
               command=self.select_all_but_first).pack(side=LEFT, padx=5)
        
        # Navigation
        nav_frame = Frame(window)
        nav_frame.pack(fill=X, padx=10, pady=10)
        
        Button(nav_frame, text="Previous", 
               command=self.prev_group).pack(side=LEFT)
        Button(nav_frame, text="Next", 
               command=self.next_group).pack(side=RIGHT)
        
        self.dup_window = window
        self.refresh_group_view()
    
    def refresh_group_view(self):
        groups = self.duplicate_finder.get_duplicate_groups()
        total = len(groups)
        idx = self.current_group_index + 1
        self.group_label_var.set(f"Group {idx} of {total} (same content)")
        
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        current_paths = groups[self.current_group_index]
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
    
    def delete_selected(self):
        groups = self.duplicate_finder.get_duplicate_groups()
        current_paths = list(groups[self.current_group_index])
        selected = self.get_selected_paths()
        
        if not selected:
            messagebox.showwarning("Delete", "No files selected.")
            return
        
        deleted, missing, errors = self._safe_delete_files(selected)
        
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
            messagebox.showerror("Delete Error", 
                f"Some files could not be moved to Recycle Bin:\n{err_text}")
        
        self._update_after_action(deleted, missing)
    
    def _safe_delete_files(self, file_paths):
        deleted = []
        missing = []
        errors = []
        
        for raw_path in file_paths:
            path = self._normalize_path(raw_path)
            
            try:
                if not os.path.exists(path):
                    missing.append(path)
                    continue
                
                try:
                    send2trash(path)
                    deleted.append(path)
                except Exception as e:
                    try:
                        fallback_dir = os.path.join(self.directory, "Duplicates_Trash")
                        os.makedirs(fallback_dir, exist_ok=True)
                        dest = self._get_unique_path(fallback_dir, os.path.basename(path))
                        shutil.move(path, dest)
                        deleted.append(path)
                    except Exception as e_move:
                        errors.append((path, f"fallback move error: {e_move}"))
            except Exception as e:
                errors.append((raw_path, str(e)))
        
        return deleted, missing, errors
    
    def _normalize_path(self, path):
        if not path:
            return path
        path = str(path)
        if path.startswith('\\\\?\\'):
            path = path[4:]
        return os.path.abspath(os.path.normpath(path))
    
    def _get_unique_path(self, directory, filename):
        dest = os.path.join(directory, filename)
        if not os.path.exists(dest):
            return dest
        
        base, ext = os.path.splitext(filename)
        i = 1
        while os.path.exists(dest):
            dest = os.path.join(directory, f"{base}({i}){ext}")
            i += 1
        return dest
    
    def move_selected(self):
        groups = self.duplicate_finder.get_duplicate_groups()
        current_paths = list(groups[self.current_group_index])
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
                os.makedirs(target_dir, exist_ok=True)
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
        
        self._update_after_action(selected, [])
    
    def keep_both(self):
        groups = self.duplicate_finder.get_duplicate_groups()
        current_paths = list(groups[self.current_group_index])
        
        self.append_log({
            "timestamp": time.time(),
            "group_index": self.current_group_index,
            "action": "skip",
            "group": current_paths
        })
        
        if self.current_group_index < len(groups) - 1:
            self.current_group_index += 1
            self.refresh_group_view()
        else:
            messagebox.showinfo("Review", "Review complete.")
            self.dup_window.destroy()
    
    def prev_group(self):
        if self.current_group_index > 0:
            self.current_group_index -= 1
            self.refresh_group_view()
    
    def next_group(self):
      
        groups = self.duplicate_finder.get_duplicate_groups()
        if self.current_group_index < len(groups) - 1:
            self.current_group_index += 1
            self.refresh_group_view()
        else:
            messagebox.showinfo("Review", "Reached last group.")
    
    def _update_after_action(self, deleted, missing):
       
        groups = self.duplicate_finder.get_duplicate_groups()
        current_paths = groups[self.current_group_index]
        
        remaining = [p for p in current_paths if p not in deleted and p not in missing]
        groups[self.current_group_index] = remaining
        
        if len(remaining) <= 1:
            del groups[self.current_group_index]
            if self.current_group_index >= len(groups):
                self.current_group_index = max(0, len(groups) - 1)
        
        if not groups:
            messagebox.showinfo("Duplicates", "No more duplicate groups.")
            self.dup_window.destroy()
            return
        
        self.refresh_group_view()
    
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