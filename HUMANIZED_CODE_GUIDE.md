# 📚 File Organizer - Core Modules Guide
## Understanding How Directory Selection, File Organization, and Undo Work

---

## 🎯 Overview

This guide explains the three essential functions that make the File Organizer work:

1. **Directory Selection** - Choosing which folder to organize
2. **File Organization** - Automatically sorting files into categories
3. **Undo Operation** - Reversing the organization if needed

Each section breaks down the code step-by-step with real examples, visual diagrams, and explanations in plain English.

---

# 📁 MODULE 1: DIRECTORY SELECTION

## What It Does

The Directory Selection module lets users choose a folder they want to organize. It also loads any custom organization rules specific to that folder.

## The Code

```python
def select_directory(self):
    """
    Open a dialog for the user to choose which folder they want to organize.
    Also loads any custom configuration specific to that directory.
    """
    # Show the folder selection dialog
    self.directory = filedialog.askdirectory()
    
    if self.directory:
        # Update status to show which folder was selected
        self.status_label.config(text=f"✓ Selected: {self.directory}")
        
        # Check if this directory has its own custom organization rules
        # (looks for .organizer_config.json in the directory)
        self.config = self.load_config(self.directory)
```

## Step-by-Step Explanation

### Step 1: Opening the Dialog Box

```python
self.directory = filedialog.askdirectory()
```

**What happens:**
- A native system dialog window pops up (looks like Windows Explorer or Mac Finder)
- User can browse their computer and click on any folder
- When they click "Select Folder", the full path is returned as a string
- If they click "Cancel", it returns an empty string `""`

**Example:**
```
User clicks: C:\Users\pranj\Documents\MyFiles
Result: self.directory = "C:\\Users\\pranj\\Documents\\MyFiles"
```

**Why this matters:**
- This path becomes the "working directory" - where all operations happen
- Everything in this folder will be organized when the user clicks "Organize Files"

### Step 2: Checking If User Actually Selected Something

```python
if self.directory:
```

**What happens:**
- Python checks if `self.directory` has a value
- Empty string `""` equals `False`, so the code inside won't run if user cancelled
- This prevents errors from trying to work with a folder that doesn't exist

**Example scenarios:**

| User Action | self.directory Value | if self.directory Result |
|-------------|---------------------|-------------------------|
| Selects folder | "C:\\Users\\pranj\\Documents" | True ✓ (runs code inside) |
| Clicks Cancel | "" | False ✗ (skips code inside) |
| Closes dialog | None | False ✗ (skips code inside) |

### Step 3: Showing Confirmation to User

```python
self.status_label.config(text=f"✓ Selected: {self.directory}")
```

**What happens:**
- Updates the label at the bottom of the window
- Uses an f-string to insert the actual folder path
- Shows a checkmark ✓ for visual confirmation

**Before and after:**

```
Before: "Welcome! Select a directory to get started."
After:  "✓ Selected: C:\Users\pranj\Documents\MyFiles"
```

**Why this is important:**
- Gives immediate feedback so user knows their click worked
- Shows exactly which folder will be organized
- Reduces confusion and mistakes

### Step 4: Loading Configuration Rules

```python
self.config = self.load_config(self.directory)
```

**What happens:**
- Calls a helper function to load organization rules
- First checks if the selected folder has its own custom config file (`.organizer_config.json`)
- If not found, uses the app-wide config file (`config.json`)
- If that's also not found, uses built-in default rules

**Configuration search priority:**
```
1. C:\Users\pranj\Documents\MyFiles\.organizer_config.json  ← Directory-specific
2. C:\Users\pranj\Desktop\projects\filorganiser\config.json  ← App-wide
3. Default rules built into the code                         ← Fallback
```

**What a config file looks like:**
```json
{
  "categories": {
    "Documents": [".pdf", ".docx", ".txt"],
    "Images": [".jpg", ".png", ".gif"],
    "Videos": [".mp4", ".avi", ".mkv"]
  },
  "default_folder": "Others"
}
```

**How it's used:**
- `.pdf` files go to "Documents" folder
- `.jpg` files go to "Images" folder
- `.xyz` files (not in any category) go to "Others" folder

## Visual Flow Diagram

```
┌─────────────────────────────────────────┐
│ User clicks "Select Directory" button   │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│ filedialog.askdirectory() opens window  │
│ (Windows Explorer / Mac Finder dialog)  │
└────────────────┬────────────────────────┘
                 │
        ┌────────┴────────┐
        │                 │
        ▼                 ▼
   User selects      User cancels
      folder             dialog
        │                 │
        │                 ▼
        │         self.directory = ""
        │         (nothing happens)
        │
        ▼
  self.directory = "C:\Users\pranj\Documents\MyFiles"
        │
        ▼
  Check if self.directory has a value
        │
        ▼ (Yes, it does)
        │
        ▼
  Update status label:
  "✓ Selected: C:\Users\pranj\Documents\MyFiles"
        │
        ▼
  Load configuration:
  self.config = load_config(directory)
        │
        ├─→ Check: Does MyFiles\.organizer_config.json exist?
        │   Yes → Load it ✓
        │   No  → Continue ↓
        │
        ├─→ Check: Does app config.json exist?
        │   Yes → Load it ✓
        │   No  → Continue ↓
        │
        └─→ Use default config (built-in)
```

## Real-World Example

**Scenario:** Sarah wants to organize her Downloads folder

1. **Sarah clicks "Select Directory" button**
   - App shows Windows folder browser

2. **Sarah navigates to C:\Users\Sarah\Downloads and clicks "Select Folder"**
   - `self.directory` now equals `"C:\\Users\\Sarah\\Downloads"`

3. **App updates the status label**
   - Shows: "✓ Selected: C:\Users\Sarah\Downloads"

4. **App looks for configuration files:**
   - Checks: `C:\Users\Sarah\Downloads\.organizer_config.json` → Not found
   - Checks: `C:\Users\pranj\Desktop\projects\filorganiser\config.json` → Found! ✓
   - Loads rules: PDFs→Documents, JPGs→Images, etc.

5. **Now Sarah is ready to click "Organize Files"**

## Key Variables

| Variable | Type | Purpose | Example Value |
|----------|------|---------|---------------|
| `self.directory` | string | Stores the selected folder path | `"C:\\Users\\pranj\\Documents"` |
| `self.config` | dictionary | Organization rules for file sorting | `{"categories": {"Images": [".jpg"]}, ...}` |
| `self.status_label` | Tkinter Label | UI element showing status messages | Label widget |

## Common Questions

**Q: What happens if I select a directory, then select a different one?**
A: The new selection replaces the old one. `self.directory` is overwritten with the new path.

**Q: Can I organize multiple folders at once?**
A: No, the app only works with one folder at a time. You'd need to select and organize each folder separately.

**Q: What if the folder I select has no files?**
A: Nothing bad happens! When you click "Organize Files", it will scan the folder, find 0 files, and report "Successfully organized 0 files!"

**Q: Does this function move any files?**
A: No! This function only SELECTS the folder. No files are moved until you click "Organize Files".

---

# 🗂️ MODULE 2: FILE ORGANIZATION

## What It Does

This is the core function that actually organizes your files. It scans every file in the selected folder, looks at each file's extension (like .pdf, .jpg, .mp3), determines which category it belongs to, creates category folders, and moves files into them.

## The Code

```python
def organize_files(self):
    """
    Main file organization function:
    1. Scans all files in the selected directory
    2. Determines the category for each file based on its extension
    3. Creates category folders if they don't exist
    4. Moves files to their appropriate category folders
    5. Tracks all moves for potential undo operation
    """
    # Safety check: make sure user selected a directory
    if not self.directory:
        self.status_label.config(text="⚠ Please select a directory first!")
        return
        
    # Clear any previous undo data - we're starting a fresh organization
    self.undo_data = []
    
    # Count how many files we organize
    files_organized = 0
    
    # Look at every item in the selected directory
    for filename in os.listdir(self.directory):
        # Build the complete path to this item
        file_path = os.path.join(self.directory, filename)
        
        # Only organize files, skip folders
        if os.path.isfile(file_path):
            # Get the file extension (e.g., ".pdf", ".jpg", ".mp3")
            file_extension = os.path.splitext(filename)[1]
            
            # Ask the config: which category does this extension belong to?
            category = self.ext_to_category(file_extension, self.config)
            
            # Build the path to the category folder
            destination = os.path.join(self.directory, category)
            
            # Create the category folder if it doesn't exist yet
            if not os.path.exists(destination):
                os.makedirs(destination)
                print(f"Created folder: {category}")
            
            # Record this move so we can undo it later if needed
            self.undo_data.append((file_path, destination))
            
            # Actually move the file!
            shutil.move(file_path, destination)
            files_organized += 1
            print(f"Moved {filename} → {category}/")
    
    # Tell the user we're done!
    self.status_label.config(text=f"✓ Successfully organized {files_organized} files!")
```

## Step-by-Step Explanation

### Step 1: Safety Check

```python
if not self.directory:
    self.status_label.config(text="⚠ Please select a directory first!")
    return
```

**What happens:**
- Checks if `self.directory` has a value
- If it's `None` or empty string, shows warning and exits the function
- `return` stops the function immediately - no files will be touched

**Why it's needed:**
- Prevents crash from trying to scan a non-existent folder
- Gives user helpful feedback about what to do

**Example scenarios:**

| Situation | self.directory | Result |
|-----------|---------------|---------|
| User never clicked "Select Directory" | None | Shows warning, exits |
| User cancelled directory selection | "" | Shows warning, exits |
| User selected a directory | "C:\Users\..." | ✓ Continues |

### Step 2: Initialize Undo Tracking

```python
self.undo_data = []
```

**What happens:**
- Creates an empty list `[]`
- Any previous undo data is erased
- This list will store information about every file we move

**Why it matters:**
- Each organization is independent - we don't mix old and new moves
- If you organize, undo, then organize again, the second organization gets fresh tracking
- Without this reset, clicking undo might try to reverse moves from previous organizations

**Data structure:**
```python
# After organizing, undo_data might look like:
[
    ("C:\\Users\\pranj\\Downloads\\report.pdf", "C:\\Users\\pranj\\Downloads\\Documents"),
    ("C:\\Users\\pranj\\Downloads\\photo.jpg", "C:\\Users\\pranj\\Downloads\\Images"),
    ("C:\\Users\\pranj\\Downloads\\song.mp3", "C:\\Users\\pranj\\Downloads\\Audio")
]
# Each tuple: (where_file_was_before, where_it_is_now)
```

### Step 3: Initialize Counter

```python
files_organized = 0
```

**What happens:**
- Creates a counter starting at 0
- Will be incremented each time we move a file
- Used at the end to tell user how many files were organized

**Why it's useful:**
- Gives concrete feedback: "Successfully organized 15 files!" is more helpful than just "Success!"
- Helps verify the operation worked as expected

### Step 4: Scan the Directory

```python
for filename in os.listdir(self.directory):
```

**What happens:**
- `os.listdir()` returns a list of everything in the folder (files AND folders)
- Loop processes each item one by one
- `filename` is just the name, not the full path (e.g., "report.pdf", not "C:\Users\...\report.pdf")

**Example:**
```python
# If directory contains:
# - report.pdf
# - photo.jpg
# - MyFolder/
# - notes.txt

# os.listdir() returns:
["report.pdf", "photo.jpg", "MyFolder", "notes.txt"]

# Loop iteration 1: filename = "report.pdf"
# Loop iteration 2: filename = "photo.jpg"
# Loop iteration 3: filename = "MyFolder"
# Loop iteration 4: filename = "notes.txt"
```

**Important note:** Only looks at items directly in the folder, not inside subfolders (not recursive)

### Step 5: Build Full Path

```python
file_path = os.path.join(self.directory, filename)
```

**What happens:**
- Combines the directory path with the filename
- Creates a complete, absolute path to the file
- `os.path.join()` handles path separators correctly (\ on Windows, / on Mac/Linux)

**Example:**
```python
self.directory = "C:\\Users\\pranj\\Downloads"
filename = "report.pdf"

file_path = os.path.join("C:\\Users\\pranj\\Downloads", "report.pdf")
# Result: "C:\\Users\\pranj\\Downloads\\report.pdf"
```

**Why we need this:**
- Most file operations need the full path, not just the filename
- `os.path.join()` prevents errors like `C:\Users\pranjDownloadsreport.pdf` (missing separator)

### Step 6: Check If It's a File (Not a Folder)

```python
if os.path.isfile(file_path):
```

**What happens:**
- `os.path.isfile()` returns `True` for files, `False` for folders
- Only files pass this check - folders are skipped
- The code inside the if-block only runs for files

**Why this is crucial:**
- We only want to organize files, not folders
- Trying to "organize" a folder would cause errors or unexpected behavior
- Existing category folders (like "Documents", "Images") are skipped automatically

**Example:**
```python
# Loop processes these items:
"report.pdf"  → os.path.isfile() = True  → Process it ✓
"photo.jpg"   → os.path.isfile() = True  → Process it ✓
"MyFolder"    → os.path.isfile() = False → Skip it ✗
"notes.txt"   → os.path.isfile() = True  → Process it ✓
```

### Step 7: Extract File Extension

```python
file_extension = os.path.splitext(filename)[1]
```

**What happens:**
- `os.path.splitext()` splits a filename into two parts: name and extension
- Returns a tuple: `(name_without_extension, extension_with_dot)`
- We take `[1]` to get just the extension

**Examples:**
```python
os.path.splitext("report.pdf")     # Returns: ("report", ".pdf")
file_extension = ... [1]            # Gets: ".pdf"

os.path.splitext("photo.jpeg")     # Returns: ("photo", ".jpeg")
file_extension = ... [1]            # Gets: ".jpeg"

os.path.splitext("README")         # Returns: ("README", "")
file_extension = ... [1]            # Gets: ""

os.path.splitext("archive.tar.gz") # Returns: ("archive.tar", ".gz")
file_extension = ... [1]            # Gets: ".gz" (only last extension!)
```

**Important notes:**
- Extension includes the dot: ".pdf", not "pdf"
- Files without extensions get empty string ""
- Files with multiple extensions only get the last one

### Step 8: Determine Category

```python
category = self.ext_to_category(file_extension, self.config)
```

**What happens:**
- Calls a helper function that looks up which category this extension belongs to
- Searches through the config file's rules
- Returns a folder name like "Documents", "Images", "Audio", or "Others"

**How `ext_to_category()` works internally:**
```python
def ext_to_category(self, ext, config):
    # Normalize extension (lowercase, ensure dot)
    ext = self.normalize_extension(ext)  # ".PDF" → ".pdf"
    
    # Search through all categories
    for folder_name, extensions in config.get('categories', {}).items():
        if ext in extensions:
            return folder_name  # Found it!
    
    # Not found in any category
    return config.get('default_folder', 'Others')
```

**Example with config:**
```json
{
  "categories": {
    "Documents": [".pdf", ".docx", ".txt"],
    "Images": [".jpg", ".png"],
    "Audio": [".mp3", ".wav"]
  },
  "default_folder": "Others"
}
```

**Lookup examples:**
```python
ext_to_category(".pdf", config)   → "Documents" (found in Documents list)
ext_to_category(".jpg", config)   → "Images"    (found in Images list)
ext_to_category(".mp3", config)   → "Audio"     (found in Audio list)
ext_to_category(".xyz", config)   → "Others"    (not found anywhere, use default)
ext_to_category("", config)       → "Others"    (empty extension, use default)
```

### Step 9: Build Destination Path

```python
destination = os.path.join(self.directory, category)
```

**What happens:**
- Combines the main directory path with the category folder name
- Creates the full path to where this file should go

**Example:**
```python
self.directory = "C:\\Users\\pranj\\Downloads"
category = "Documents"

destination = os.path.join("C:\\Users\\pranj\\Downloads", "Documents")
# Result: "C:\\Users\\pranj\\Downloads\\Documents"
```

**Visual representation:**
```
Main directory: C:\Users\pranj\Downloads\
Category folder: Documents\
Destination:     C:\Users\pranj\Downloads\Documents\
```

### Step 10: Create Category Folder If Needed

```python
if not os.path.exists(destination):
    os.makedirs(destination)
    print(f"Created folder: {category}")
```

**What happens:**
- `os.path.exists()` checks if the folder already exists
- If it doesn't exist, `os.makedirs()` creates it
- Prints a message for debugging/logging

**Why we check first:**
- Creating a folder that already exists would cause an error
- First file with `.pdf` extension creates "Documents" folder
- Subsequent PDF files find the folder already exists and skip creation

**Example timeline:**
```
Initial state:
C:\Users\pranj\Downloads\
  ├── file1.pdf
  ├── file2.jpg
  └── file3.pdf

Processing file1.pdf (.pdf → Documents):
  Check: Does Downloads\Documents exist? NO
  Create: Downloads\Documents\
  Print: "Created folder: Documents"

Processing file2.jpg (.jpg → Images):
  Check: Does Downloads\Images exist? NO
  Create: Downloads\Images\
  Print: "Created folder: Images"

Processing file3.pdf (.pdf → Documents):
  Check: Does Downloads\Documents exist? YES
  Skip creation (folder already exists)
```

### Step 11: Record for Undo

```python
self.undo_data.append((file_path, destination))
```

**What happens:**
- Creates a tuple with two pieces of information
- Adds it to the `undo_data` list
- This data allows us to reverse this move later

**Tuple structure:**
```python
(
    file_path,    # Original full path including filename
    destination   # Category folder path (NOT including filename)
)
```

**Example:**
```python
file_path = "C:\\Users\\pranj\\Downloads\\report.pdf"
destination = "C:\\Users\\pranj\\Downloads\\Documents"

self.undo_data.append(
    ("C:\\Users\\pranj\\Downloads\\report.pdf", 
     "C:\\Users\\pranj\\Downloads\\Documents")
)
```

**Why this structure:**
- `file_path` gives us the original filename
- `destination` tells us where the file is now
- Together, these let us move the file back during undo

**After organizing 3 files:**
```python
self.undo_data = [
    ("C:\\Users\\pranj\\Downloads\\report.pdf", "C:\\Users\\pranj\\Downloads\\Documents"),
    ("C:\\Users\\pranj\\Downloads\\photo.jpg", "C:\\Users\\pranj\\Downloads\\Images"),
    ("C:\\Users\\pranj\\Downloads\\song.mp3", "C:\\Users\\pranj\\Downloads\\Audio")
]
```

### Step 12: Move the File!

```python
shutil.move(file_path, destination)
files_organized += 1
print(f"Moved {filename} → {category}/")
```

**What happens:**
- `shutil.move()` physically moves the file from its current location to the destination folder
- Increments the counter: `files_organized = files_organized + 1`
- Prints a confirmation message

**The actual move:**
```python
# Before:
C:\Users\pranj\Downloads\
  └── report.pdf  ← File is here

# Move command:
shutil.move(
    "C:\\Users\\pranj\\Downloads\\report.pdf",      # From
    "C:\\Users\\pranj\\Downloads\\Documents"         # To
)

# After:
C:\Users\pranj\Downloads\
  └── Documents\
      └── report.pdf  ← File moved here
```

**Important details:**
- This is a MOVE, not a COPY - original file disappears from old location
- If a file with the same name exists in destination, it will be overwritten!
- The operation happens immediately - it's not a preview or simulation

**Counter increment:**
```python
# First file:  files_organized = 0 + 1 = 1
# Second file: files_organized = 1 + 1 = 2
# Third file:  files_organized = 2 + 1 = 3
```

### Step 13: Report Success

```python
self.status_label.config(text=f"✓ Successfully organized {files_organized} files!")
```

**What happens:**
- Updates the status label with final count
- Uses f-string to insert the actual number
- Shows checkmark for positive feedback

**Examples:**
```python
# If 0 files organized:
"✓ Successfully organized 0 files!"

# If 1 file organized:
"✓ Successfully organized 1 files!"  # (grammatically awkward but functional)

# If 15 files organized:
"✓ Successfully organized 15 files!"
```

## Complete Example

**Starting directory:**
```
C:\Users\pranj\Downloads\
  ├── vacation.jpg
  ├── report.pdf
  ├── song.mp3
  ├── notes.txt
  ├── MyFolder\
  └── unknown.xyz
```

**Configuration:**
```json
{
  "categories": {
    "Documents": [".pdf", ".txt"],
    "Images": [".jpg"],
    "Audio": [".mp3"]
  },
  "default_folder": "Others"
}
```

**Execution flow:**

| File | Is File? | Extension | Category | Action |
|------|----------|-----------|----------|--------|
| vacation.jpg | ✓ Yes | .jpg | Images | Move to Images/ |
| report.pdf | ✓ Yes | .pdf | Documents | Move to Documents/ |
| song.mp3 | ✓ Yes | .mp3 | Audio | Move to Audio/ |
| notes.txt | ✓ Yes | .txt | Documents | Move to Documents/ |
| MyFolder | ✗ No | N/A | N/A | Skip (it's a folder) |
| unknown.xyz | ✓ Yes | .xyz | Others | Move to Others/ |

**After organization:**
```
C:\Users\pranj\Downloads\
  ├── Documents\
  │   ├── report.pdf
  │   └── notes.txt
  ├── Images\
  │   └── vacation.jpg
  ├── Audio\
  │   └── song.mp3
  ├── Others\
  │   └── unknown.xyz
  └── MyFolder\  ← Untouched
```

**Final status:**
```
"✓ Successfully organized 5 files!"
```

**Undo data stored:**
```python
[
    ("C:\\Users\\pranj\\Downloads\\vacation.jpg", "C:\\Users\\pranj\\Downloads\\Images"),
    ("C:\\Users\\pranj\\Downloads\\report.pdf", "C:\\Users\\pranj\\Downloads\\Documents"),
    ("C:\\Users\\pranj\\Downloads\\song.mp3", "C:\\Users\\pranj\\Downloads\\Audio"),
    ("C:\\Users\\pranj\\Downloads\\notes.txt", "C:\\Users\\pranj\\Downloads\\Documents"),
    ("C:\\Users\\pranj\\Downloads\\unknown.xyz", "C:\\Users\\pranj\\Downloads\\Others")
]
```

## Visual Flow Diagram

```
START: User clicks "Organize Files"
  │
  ▼
┌─────────────────────────────────┐
│ Check: Is directory selected?   │
└───────┬─────────────────────────┘
        │
   ┌────┴────┐
   NO        YES
   │         │
   ▼         ▼
Show error   Clear undo_data = []
Exit         files_organized = 0
             │
             ▼
┌────────────────────────────────────┐
│ Loop through os.listdir(directory) │
└────────────┬───────────────────────┘
             │
             ▼ (for each item)
┌────────────────────────────────┐
│ Build full path: file_path     │
└────────────┬───────────────────┘
             │
             ▼
┌──────────────────────────────┐
│ Check: Is it a file?         │
└───────┬──────────────────────┘
        │
   ┌────┴────┐
   NO        YES
   │         │
   ▼         ▼
Skip it     Extract extension
Continue    │
loop        ▼
            Lookup category
            │
            ▼
            Build destination path
            │
            ▼
            Check: Does category folder exist?
            │
       ┌────┴────┐
       NO        YES
       │         │
       ▼         ▼
    Create      Skip
    folder      creation
       │         │
       └────┬────┘
            │
            ▼
            Record to undo_data
            │
            ▼
            Move file to destination
            │
            ▼
            Increment files_organized
            │
            ▼
        Continue to next file
            │
            ▼
    (Loop ends when no more files)
            │
            ▼
┌─────────────────────────────────────┐
│ Update status with files_organized  │
│ "✓ Successfully organized X files!" │
└─────────────────────────────────────┘
            │
            ▼
           END
```

## Key Variables

| Variable | Type | Scope | Purpose | Example Value |
|----------|------|-------|---------|---------------|
| `self.directory` | string | Instance | Selected folder path | `"C:\\Users\\pranj\\Downloads"` |
| `self.config` | dict | Instance | Organization rules | `{"categories": {...}, "default_folder": "Others"}` |
| `self.undo_data` | list | Instance | Tracks moves for undo | `[(...), (...), ...]` |
| `files_organized` | int | Function | Counts moved files | `5` |
| `filename` | string | Loop | Current item name | `"report.pdf"` |
| `file_path` | string | Loop | Full path to file | `"C:\\...\\report.pdf"` |
| `file_extension` | string | Loop | File extension | `".pdf"` |
| `category` | string | Loop | Destination folder name | `"Documents"` |
| `destination` | string | Loop | Full path to category | `"C:\\...\\Documents"` |

## Common Questions

**Q: What happens to files without extensions?**
A: Files without extensions (like "README" or "config") get an empty string `""` as their extension, which doesn't match any category, so they go to the "Others" folder.

**Q: Can two files with the same name be organized?**
A: If two files have the same name but different extensions (like "report.pdf" and "report.jpg"), they go to different folders and there's no conflict. But if two files have the exact same name AND extension, the second one will overwrite the first!

**Q: What if a file is locked or in use?**
A: `shutil.move()` will throw an exception. Currently, the code doesn't handle this - the program would crash. Better error handling would catch the exception and continue with other files.

**Q: Does this work recursively (organize files in subfolders)?**
A: No. `os.listdir()` only looks at files directly in the selected folder. Files inside subfolders are not touched.

**Q: What if I organize the same folder twice?**
A: The second organization will look at the category folders (Documents, Images, etc.) and skip them because `os.path.isfile()` returns False for folders. So organizing twice does nothing (files are already organized).

---

# ↩️ MODULE 3: UNDO OPERATION

## What It Does

The Undo Operation reverses the last file organization by moving all files back to their original locations in the main directory. It's like a "ctrl+Z" for file organization.

## The Code

```python
def undo(self):
    """
    Reverses the last file organization operation by moving all files
    back to their original locations.
    
    Note: Only works for the most recent organization. If you organize twice,
    you can only undo the second operation.
    """
    # Check if there's anything to undo
    if not self.undo_data:
        self.status_label.config(text="ℹ Nothing to undo.")
        return
    
    # Move each file back to its original location
    files_restored = 0
    
    for original_path, category_folder in self.undo_data:
        # Extract just the filename from the original path
        filename = os.path.basename(original_path)
        
        # Build the current location (where the file is now)
        current_location = os.path.join(category_folder, filename)
        
        # Move it back to the main directory
        try:
            shutil.move(current_location, self.directory)
            files_restored += 1
            print(f"Restored: {filename}")
        except Exception as error:
            print(f"Failed to restore {filename}: {error}")
    
    # Clear the undo data - we can't undo twice
    self.undo_data = []
    
    # Tell the user we're done
    self.status_label.config(text=f"✓ Restored {files_restored} files to original location!")
```

## Step-by-Step Explanation

### Step 1: Check If Undo Is Possible

```python
if not self.undo_data:
    self.status_label.config(text="ℹ Nothing to undo.")
    return
```

**What happens:**
- Checks if `self.undo_data` list has any items
- Empty list `[]` evaluates to `False` in a boolean context
- If empty, shows message and exits function immediately

**When is undo_data empty?**

| Situation | undo_data Value | Result |
|-----------|----------------|---------|
| Just opened the app | `[]` | Show "Nothing to undo" |
| Selected directory but didn't organize | `[]` | Show "Nothing to undo" |
| Organized files | `[(...), (...)]` | ✓ Proceed with undo |
| Already clicked undo once | `[]` | Show "Nothing to undo" |

**Why this check is crucial:**
- Prevents errors from trying to undo when there's no data
- Gives user clear feedback about why undo isn't working
- `return` statement stops function execution

### Step 2: Initialize Counter

```python
files_restored = 0
```

**What happens:**
- Creates a counter starting at 0
- Will be incremented for each file successfully moved back
- Used to show user how many files were restored

**Why count separately:**
- Some files might fail to restore (deleted, moved manually, permissions, etc.)
- This lets us report: "Restored 4 out of 5 files" if one failed

### Step 3: Loop Through Undo Data

```python
for original_path, category_folder in self.undo_data:
```

**What happens:**
- Loops through each tuple in the `undo_data` list
- Unpacks each tuple into two variables automatically
- Processes each moved file one by one

**Unpacking explained:**
```python
# If undo_data contains:
[
    ("C:\\Users\\pranj\\Downloads\\report.pdf", "C:\\Users\\pranj\\Downloads\\Documents"),
    ("C:\\Users\\pranj\\Downloads\\photo.jpg", "C:\\Users\\pranj\\Downloads\\Images")
]

# Loop iteration 1:
original_path = "C:\\Users\\pranj\\Downloads\\report.pdf"
category_folder = "C:\\Users\\pranj\\Downloads\\Documents"

# Loop iteration 2:
original_path = "C:\\Users\\pranj\\Downloads\\photo.jpg"
category_folder = "C:\\Users\\pranj\\Downloads\\Images"
```

**Visual representation:**
```
undo_data = [
    (  ─────────────original_path────────────, ──category_folder──  )
    ("C:\\Users\\pranj\\Downloads\\report.pdf", "...\\Documents"    ),
    ("C:\\Users\\pranj\\Downloads\\photo.jpg",  "...\\Images"       )
]
```

### Step 4: Extract Filename

```python
filename = os.path.basename(original_path)
```

**What happens:**
- `os.path.basename()` extracts just the filename from a full path
- Removes all directory information
- Returns only the last part of the path

**Examples:**
```python
os.path.basename("C:\\Users\\pranj\\Downloads\\report.pdf")
# Returns: "report.pdf"

os.path.basename("C:\\Users\\pranj\\Documents\\vacation.jpg")
# Returns: "vacation.jpg"

os.path.basename("C:\\Windows\\System32\\notepad.exe")
# Returns: "notepad.exe"
```

**Why we need just the filename:**
- `original_path` is where the file WAS before organization
- The file isn't there anymore - it's in the category folder
- We need the filename to locate it in the category folder

**The situation:**
```
original_path = "C:\\Users\\pranj\\Downloads\\report.pdf"
                                                  ^^^^^^^^^^^
                                                  We need this part
File is now at: "C:\\Users\\pranj\\Downloads\\Documents\\report.pdf"
```

### Step 5: Build Current Location

```python
current_location = os.path.join(category_folder, filename)
```

**What happens:**
- Combines the category folder path with the filename
- Creates the full path to where the file currently is (after organization)
- This is where we need to move the file FROM

**Example:**
```python
category_folder = "C:\\Users\\pranj\\Downloads\\Documents"
filename = "report.pdf"

current_location = os.path.join(
    "C:\\Users\\pranj\\Downloads\\Documents",
    "report.pdf"
)
# Result: "C:\\Users\\pranj\\Downloads\\Documents\\report.pdf"
```

**Visual timeline:**
```
BEFORE ORGANIZATION:
File location: C:\Users\pranj\Downloads\report.pdf
                           (stored in original_path)

AFTER ORGANIZATION:
File location: C:\Users\pranj\Downloads\Documents\report.pdf
                           (calculated as current_location)

FOR UNDO, WE NEED TO:
Move from: current_location (C:\...\Downloads\Documents\report.pdf)
Move to:   self.directory   (C:\...\Downloads\)
```

### Step 6: Move File Back (with Error Handling)

```python
try:
    shutil.move(current_location, self.directory)
    files_restored += 1
    print(f"Restored: {filename}")
except Exception as error:
    print(f"Failed to restore {filename}: {error}")
```

**What happens:**
- Attempts to move the file back to the main directory
- If successful: increments counter and prints confirmation
- If fails: catches the error and prints what went wrong, but continues with other files

**The try-except structure:**

```python
try:
    # Try to do this (might fail)
    risky_operation()
except Exception:
    # If it fails, do this instead (doesn't crash)
    handle_error()
```

**Why error handling is important:**
- File might have been manually deleted
- File might have been moved elsewhere by user
- Permission issues
- Disk errors
- Without try-except, one failure would crash the entire undo operation

**Example scenarios:**

| Situation | Result |
|-----------|--------|
| File exists in category folder, undo works | ✓ File moved, counter++, print success |
| User manually deleted the file | ✗ Exception caught, print error, continue to next file |
| User manually moved file to Desktop | ✗ Exception caught, print error, continue to next file |
| File is open in another program | ✗ Exception caught, print error, continue to next file |

**The actual move:**
```python
# Before undo:
C:\Users\pranj\Downloads\
  └── Documents\
      └── report.pdf  ← File is here

# shutil.move command:
shutil.move(
    "C:\\Users\\pranj\\Downloads\\Documents\\report.pdf",  # From (current_location)
    "C:\\Users\\pranj\\Downloads\\"                         # To (self.directory)
)

# After undo:
C:\Users\pranj\Downloads\
  ├── report.pdf  ← File moved back!
  └── Documents\  ← Empty folder remains
```

**Counter increment:**
```python
# First file restored:  files_restored = 0 + 1 = 1
# Second file restored: files_restored = 1 + 1 = 2
# Third file restored:  files_restored = 2 + 1 = 3
```

### Step 7: Clear Undo Data

```python
self.undo_data = []
```

**What happens:**
- Empties the undo_data list
- All move records are deleted
- The variable now contains an empty list `[]`

**Why clear it:**
- You can't undo the same operation twice - files are already back where they started
- If user organizes again, we need fresh tracking
- Prevents confusion about what undo will do

**Timeline:**
```
After organizing:
self.undo_data = [(...), (...), (...)]  # 3 moves recorded

After clicking undo:
self.undo_data = []  # Cleared

If user clicks undo again:
"ℹ Nothing to undo."  # No data to work with
```

### Step 8: Report Success

```python
self.status_label.config(text=f"✓ Restored {files_restored} files to original location!")
```

**What happens:**
- Updates status label with confirmation message
- Uses f-string to show exact number of files restored
- Checkmark gives positive feedback

**Example messages:**
```python
# All 5 files restored successfully:
"✓ Restored 5 files to original location!"

# 4 out of 5 files restored (1 failed):
"✓ Restored 4 files to original location!"

# No files restored (all failed):
"✓ Restored 0 files to original location!"
```

**Note:** Currently doesn't distinguish between "all succeeded" vs "some failed". Better implementation would say: "Restored 4 out of 5 files (1 error)"

## Complete Example

**After organization:**
```
C:\Users\pranj\Downloads\
  ├── Documents\
  │   ├── report.pdf
  │   └── notes.txt
  ├── Images\
  │   └── vacation.jpg
  └── Audio\
      └── song.mp3

self.undo_data = [
    ("C:\\Users\\pranj\\Downloads\\report.pdf", "C:\\Users\\pranj\\Downloads\\Documents"),
    ("C:\\Users\\pranj\\Downloads\\notes.txt", "C:\\Users\\pranj\\Downloads\\Documents"),
    ("C:\\Users\\pranj\\Downloads\\vacation.jpg", "C:\\Users\\pranj\\Downloads\\Images"),
    ("C:\\Users\\pranj\\Downloads\\song.mp3", "C:\\Users\\pranj\\Downloads\\Audio")
]
```

**User clicks "Undo" button**

**Loop iteration 1:**
```python
original_path = "C:\\Users\\pranj\\Downloads\\report.pdf"
category_folder = "C:\\Users\\pranj\\Downloads\\Documents"
filename = "report.pdf"
current_location = "C:\\Users\\pranj\\Downloads\\Documents\\report.pdf"

Move: Documents\report.pdf → Downloads\
Result: ✓ Success
files_restored = 1
```

**Loop iteration 2:**
```python
original_path = "C:\\Users\\pranj\\Downloads\\notes.txt"
category_folder = "C:\\Users\\pranj\\Downloads\\Documents"
filename = "notes.txt"
current_location = "C:\\Users\\pranj\\Downloads\\Documents\\notes.txt"

Move: Documents\notes.txt → Downloads\
Result: ✓ Success
files_restored = 2
```

**Loop iteration 3:**
```python
original_path = "C:\\Users\\pranj\\Downloads\\vacation.jpg"
category_folder = "C:\\Users\\pranj\\Downloads\\Images"
filename = "vacation.jpg"
current_location = "C:\\Users\\pranj\\Downloads\\Images\\vacation.jpg"

Move: Images\vacation.jpg → Downloads\
Result: ✓ Success
files_restored = 3
```

**Loop iteration 4:**
```python
original_path = "C:\\Users\\pranj\\Downloads\\song.mp3"
category_folder = "C:\\Users\\pranj\\Downloads\\Audio"
filename = "song.mp3"
current_location = "C:\\Users\\pranj\\Downloads\\Audio\\song.mp3"

Move: Audio\song.mp3 → Downloads\
Result: ✓ Success
files_restored = 4
```

**After undo:**
```
C:\Users\pranj\Downloads\
  ├── report.pdf      ← Restored!
  ├── notes.txt       ← Restored!
  ├── vacation.jpg    ← Restored!
  ├── song.mp3        ← Restored!
  ├── Documents\      ← Empty folder remains
  ├── Images\         ← Empty folder remains
  └── Audio\          ← Empty folder remains

self.undo_data = []  # Cleared

Status: "✓ Restored 4 files to original location!"
```

## Visual Flow Diagram

```
START: User clicks "Undo"
  │
  ▼
┌──────────────────────────────┐
│ Check: Is undo_data empty?   │
└───────┬──────────────────────┘
        │
   ┌────┴────┐
   YES       NO
   │         │
   ▼         ▼
Show msg    files_restored = 0
"Nothing    │
to undo"    ▼
Exit      ┌─────────────────────────────┐
          │ Loop through undo_data      │
          └────────┬────────────────────┘
                   │
                   ▼ (for each tuple)
          ┌─────────────────────────────┐
          │ Unpack: original_path,      │
          │         category_folder     │
          └────────┬────────────────────┘
                   │
                   ▼
          ┌─────────────────────────────┐
          │ Extract filename from path  │
          └────────┬────────────────────┘
                   │
                   ▼
          ┌─────────────────────────────┐
          │ Build current_location      │
          │ (category_folder + filename)│
          └────────┬────────────────────┘
                   │
                   ▼
          ┌─────────────────────────────┐
          │ TRY: Move file back         │
          │ From: current_location      │
          │ To: self.directory          │
          └────────┬────────────────────┘
                   │
          ┌────────┴─────────┐
      Success          Error
          │              │
          ▼              ▼
  Increment counter  Print error
  Print success      Continue loop
          │              │
          └──────┬───────┘
                 │
                 ▼
         Continue to next file
                 │
                 ▼
      (Loop ends when no more moves)
                 │
                 ▼
          ┌──────────────────────────┐
          │ Clear undo_data = []     │
          └──────────┬───────────────┘
                     │
                     ▼
          ┌──────────────────────────────────┐
          │ Update status with count         │
          │ "✓ Restored X files..."          │
          └──────────────────────────────────┘
                     │
                     ▼
                    END
```

## Key Variables

| Variable | Type | Scope | Purpose | Example Value |
|----------|------|-------|---------|---------------|
| `self.undo_data` | list | Instance | Stores moves to reverse | `[(...), (...)]` |
| `self.directory` | string | Instance | Main directory path | `"C:\\Users\\pranj\\Downloads"` |
| `files_restored` | int | Function | Counts successful restores | `4` |
| `original_path` | string | Loop | Path before organization | `"C:\\...\\Downloads\\report.pdf"` |
| `category_folder` | string | Loop | Category folder path | `"C:\\...\\Downloads\\Documents"` |
| `filename` | string | Loop | Just the filename | `"report.pdf"` |
| `current_location` | string | Loop | Where file is now | `"C:\\...\\Documents\\report.pdf"` |

## Important Limitations

### 1. Single-Level Undo Only

```python
# First organization:
organize_files()  
# undo_data = [move1, move2, move3]

# Second organization:
organize_files()  
# undo_data = [move4, move5]  ← First organization data LOST!

# Clicking undo:
undo()  
# Only reverses the SECOND organization
```

**Why:** `self.undo_data = []` at the start of `organize_files()` wipes out previous data

**To fix:** Would need to store a history of undo_data lists (stack structure)

### 2. Assumes Filename Unchanged

```python
# After organization:
"C:\\Users\\pranj\\Downloads\\Documents\\report.pdf"

# User manually renames:
"C:\\Users\\pranj\\Downloads\\Documents\\quarterly_report.pdf"

# Undo tries to find:
filename = "report.pdf"  # From original_path
current_location = "...\\Documents\\report.pdf"  # Doesn't exist!

# Result: Exception, print error, continue
```

**Why:** We only store the original filename, not the current filename

**To fix:** Would need to search for the file or store the hash

### 3. No Error Reporting to User

```python
try:
    shutil.move(current_location, self.directory)
    files_restored += 1
    print(f"Restored: {filename}")
except Exception as error:
    print(f"Failed to restore {filename}: {error}")  # Only prints to console!
```

**Problem:** Errors only print to console, user doesn't see them in the GUI

**Result:** Status might say "Restored 3 files!" but user doesn't know 2 failed

**To fix:** Collect errors in a list and show them in a message box

### 4. Not Persistent

```python
# User organizes files:
self.undo_data = [(...), (...), (...)]  # Stored in RAM

# User closes application:
# undo_data is lost forever

# User reopens application:
self.undo_data = []  # Fresh start, can't undo previous session
```

**Why:** Data only exists in memory, not saved to disk

**To fix:** Save undo_data to a JSON file, load it when app starts

### 5. Empty Folders Remain

```python
# After undo, category folders still exist but are empty:
C:\Users\pranj\Downloads\
  ├── report.pdf      ← Restored
  ├── Documents\      ← Empty folder remains
  └── Images\         ← Empty folder remains
```

**Why:** Undo only moves files back, doesn't delete folders

**To fix:** Add code to detect and remove empty folders:
```python
try:
    os.rmdir(category_folder)  # Only works if folder is empty
except OSError:
    pass  # Folder not empty or other issue, ignore
```

## Common Questions

**Q: Can I undo multiple times?**
A: No. After the first undo, `self.undo_data` is cleared. Clicking undo again shows "Nothing to undo."

**Q: What if I manually move a file after organizing?**
A: Undo will fail for that specific file (exception caught), but other files will still be restored.

**Q: Can I undo after closing and reopening the app?**
A: No. Undo data is not saved to disk, so it's lost when you close the app.

**Q: What if two files had the same name (like "report.pdf" in Documents and Images)?**
A: During undo, the second file would overwrite the first when both are moved back to the main directory. Data loss would occur!

**Q: Does undo delete the category folders?**
A: No. Empty category folders remain after undo. You can manually delete them if desired.

**Q: Can I partially undo (just some files)?**
A: No. Undo is all-or-nothing - it processes everything in undo_data.

---

## 🔗 How the Three Modules Work Together

```
┌─────────────────────────────────────────────────────────────┐
│                    USER WORKFLOW                             │
└─────────────────────────────────────────────────────────────┘

1. DIRECTORY SELECTION
   ↓
   User clicks "Select Directory"
   ↓
   select_directory() runs
   ↓
   self.directory = "C:\\Users\\pranj\\Downloads"
   self.config = {categorization rules}
   ↓
   Status: "✓ Selected: C:\\Users\\pranj\\Downloads"

2. FILE ORGANIZATION
   ↓
   User clicks "Organize Files"
   ↓
   organize_files() runs
   ↓
   self.undo_data = []  # Reset
   ↓
   For each file:
     - Extract extension
     - Lookup category
     - Create category folder
     - Record to undo_data
     - Move file
   ↓
   Status: "✓ Successfully organized 15 files!"
   self.undo_data = [(file1, cat1), (file2, cat2), ...]

3. UNDO OPERATION (if needed)
   ↓
   User clicks "Undo"
   ↓
   undo() runs
   ↓
   For each move in undo_data:
     - Extract filename
     - Build current location
     - Move file back
   ↓
   self.undo_data = []  # Clear
   ↓
   Status: "✓ Restored 15 files to original location!"
```

## Data Flow Between Modules

```
┌──────────────────┐
│ select_directory │
└────────┬─────────┘
         │ Sets
         ▼
    self.directory ────────┐
    self.config            │
         │                 │
         │ Used by         │ Used by
         ▼                 │
┌─────────────────┐        │
│ organize_files  │        │
└────────┬────────┘        │
         │ Creates         │
         ▼                 │
    self.undo_data         │
         │                 │
         │ Used by         │
         ▼                 │
    ┌─────────┐            │
    │  undo   │ ←──────────┘
    └─────────┘ Also uses self.directory
```

## Variable Lifecycle

| Variable | Created By | Modified By | Used By | Cleared By |
|----------|-----------|-------------|---------|------------|
| `self.directory` | select_directory() | select_directory() | organize_files(), undo() | - |
| `self.config` | \_\_init\_\_(), select_directory() | load_config() | organize_files() | - |
| `self.undo_data` | \_\_init\_\_() | organize_files() | undo() | organize_files(), undo() |

---

## 💡 Quick Reference

### Directory Selection
- **Purpose:** Choose folder to organize
- **Input:** User clicks "Select Directory"
- **Output:** Sets `self.directory` and loads `self.config`
- **Side effects:** None (no files touched)

### File Organization
- **Purpose:** Sort files into category folders
- **Input:** Requires `self.directory` and `self.config`
- **Output:** Files moved, `self.undo_data` populated
- **Side effects:** Creates folders, moves files

### Undo Operation
- **Purpose:** Reverse last organization
- **Input:** Requires `self.undo_data` and `self.directory`
- **Output:** Files moved back
- **Side effects:** Clears `self.undo_data`, leaves empty folders

---

## 🎓 Key Takeaways

1. **Directory Selection** sets up the workspace and rules
2. **File Organization** does the actual work and creates an audit trail
3. **Undo Operation** uses the audit trail to reverse changes
4. All three modules are interconnected through shared variables
5. Error handling could be improved in all three modules
6. Undo is single-level only - can't undo multiple operations

---

*This guide was created to help understand the core functionality of the File Organizer application. For questions or improvements, refer to the actual code with its inline comments.*
