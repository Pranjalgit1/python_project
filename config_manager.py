import os
import json
import shutil
import time
from tkinter import Toplevel, Frame, Button, Label, Entry, Listbox, StringVar
from tkinter import LEFT, RIGHT, W, X, Y, END, simpledialog

class ConfigManager:
    
    def __init__(self):
        self.config = self.load_config()
    
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
        norm = {
            "categories": {}, 
            "default_folder": self.sanitize_folder_name(default_folder)
        }

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
                        config = self.normalize_config(json.load(f))
                        self.config = config
                        return config
            except Exception:
                pass
        
        p = self.app_config_path()
        try:
            if os.path.exists(p):
                with open(p, 'r', encoding='utf-8') as f:
                    config = self.normalize_config(json.load(f))
                    self.config = config
                    return config
        except Exception:
            pass
        
        config = self.default_config()
        self.config = config
        return config
    
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
        
        self.config = cfg
        return cfg
    
    def get_config(self):
   
        return self.config
    
    def ext_to_category(self, ext):
        ext = self.normalize_extension(ext)
        for folder, exts in self.config.get('categories', {}).items():
            if ext in exts:
                return folder
        return self.config.get('default_folder', 'Others')
    
    def open_categories_editor(self, root, directory=None):
        cfg = json.loads(json.dumps(self.config))
        
        win = Toplevel(root)
        win.title("Custom Categories")
        win.geometry("700x420")
        
        left = Frame(win)
        left.pack(side=LEFT, fill=Y, padx=10, pady=10)
        
        Label(left, text="Categories").pack(anchor=W)
        cat_list = Listbox(left, height=18)
        cat_list.pack(fill=Y)
        
        right = Frame(win)
        right.pack(side=RIGHT, fill="both", expand=True, padx=10, pady=10)
        
        Label(right, text="Default Folder").pack(anchor=W)
        default_var = StringVar(value=cfg.get('default_folder', 'Others'))
        Entry(right, textvariable=default_var).pack(fill=X)
        
        Label(right, text="Extensions (comma-separated)").pack(anchor=W, pady=(10, 0))
        exts_var = StringVar(value="")
        Entry(right, textvariable=exts_var).pack(fill=X)
        
        msg_var = StringVar(value="")
        Label(right, textvariable=msg_var, fg="red").pack(anchor=W, pady=(6, 0))
        
        def refresh_list():
            cat_list.delete(0, END)
            for folder in sorted(cfg['categories'].keys()):
                cat_list.insert(END, folder)
        
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
            
            self.save_config(cfg, directory=directory)
            win.destroy()
        
        Button(left, text="Add Category", command=add_category).pack(fill=X, pady=(8, 2))
        Button(left, text="Delete Category", command=delete_category).pack(fill=X)
        Button(right, text="Save & Close", command=save_close).pack(anchor="e", pady=(12, 0))
        Button(right, text="Cancel", command=win.destroy).pack(anchor="e")
        
        refresh_list()