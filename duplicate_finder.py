import os
import hashlib

class DuplicateFinder:

    
    def __init__(self):
        self.hash_to_paths = {}
        self.duplicate_groups = []
    
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
    
    def scan_directory(self, directory):
       
        self.hash_to_paths = {}
        
        for root_dir, _, files in os.walk(directory):
            for name in files:
                file_path = os.path.join(root_dir, name)
                
                if not os.path.isfile(file_path):
                    continue
                
                file_hash = self.compute_file_hash(file_path)
                if not file_hash:
                    continue
                
                self.hash_to_paths.setdefault(file_hash, []).append(file_path)
        
        self.duplicate_groups = [
            paths for paths in self.hash_to_paths.values() 
            if len(paths) > 1
        ]
        
        return self.duplicate_groups
    
    def get_duplicate_groups(self):
        
        return self.duplicate_groups