from tkinter import Toplevel, Frame, Button
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import os
from collections import defaultdict

class StatisticsDashboard:
    
    def __init__(self, parent, directory, config_manager):
        self.parent = parent
        self.directory = directory
        self.config_manager = config_manager
        self.window = Toplevel(parent)
        self.window.title("File Statistics Dashboard")
        self.window.geometry("1000x700")
        self.analyze_files()
        self.setup_ui()
    
    def analyze_files(self):
        self.category_count = defaultdict(int)
        self.category_size = defaultdict(int)
        self.extension_count = defaultdict(int)
        self.total_files = 0
        self.total_size = 0
        if not self.directory or not os.path.exists(self.directory):
            return
        for root_dir, _, files in os.walk(self.directory):
            for filename in files:
                file_path = os.path.join(root_dir, filename)
                if os.path.isfile(file_path):
                    self.total_files += 1
                    # Get file size
                    try:
                        size = os.path.getsize(file_path)
                        self.total_size += size
                    except:
                        size = 0
                    
                    # Get extension and category
                    ext = os.path.splitext(filename)[1].lower()
                    category = self.config_manager.ext_to_category(ext)
                    self.category_count[category] += 1
                    self.category_size[category] += size
                    self.extension_count[ext] += 1
    
    def setup_ui(self):
     
        fig = Figure(figsize=(10, 7), facecolor='#f0f0f0')
        
        # Plot 1: Files by Category (Pie Chart)
        ax1 = fig.add_subplot(2, 2, 1)
        self.plot_category_pie(ax1)
        
        # Plot 2: File Count by Category (Bar Chart)
        ax2 = fig.add_subplot(2, 2, 2)
        self.plot_category_bar(ax2)
        
        # Plot 3: Storage Size by Category (Horizontal Bar)
        ax3 = fig.add_subplot(2, 2, 3)
        self.plot_size_bar(ax3)
        
        # Plot 4: Top Extensions (Bar Chart)
        ax4 = fig.add_subplot(2, 2, 4)
        self.plot_extension_bar(ax4)
        
        fig.tight_layout(pad=3.0)
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
        # Button frame
        button_frame = Frame(self.window)
        button_frame.pack(pady=10)
        
        Button(button_frame, text="Close", command=self.window.destroy,
               bg="#2196F3", fg="white", font=("Arial", 10, "bold"),
               padx=20, pady=5).pack()
    
    def plot_category_pie(self, ax):
        if not self.category_count:
            ax.text(0.5, 0.5, 'No data available', 
                   ha='center', va='center', transform=ax.transAxes)
            ax.set_title('Files by Category')
            return
        categories = list(self.category_count.keys())
        counts = list(self.category_count.values())
        colors = plt.cm.Set3(range(len(categories)))
        ax.pie(counts, labels=categories, autopct='%1.1f%%', 
               colors=colors, startangle=90)
        ax.set_title(f'Files by Category\nTotal: {self.total_files} files', 
                     fontweight='bold', fontsize=12)
    
    def plot_category_bar(self, ax):
        if not self.category_count:
            ax.text(0.5, 0.5, 'No data available', 
                   ha='center', va='center', transform=ax.transAxes)
            ax.set_title('File Count by Category')
            return
        categories = list(self.category_count.keys())
        counts = list(self.category_count.values())
        colors = plt.cm.Paired(range(len(categories)))
        bars = ax.bar(categories, counts, color=colors, edgecolor='black', linewidth=0.5)
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}', ha='center', va='bottom', fontsize=9)
        
        ax.set_xlabel('Category', fontweight='bold')
        ax.set_ylabel('Number of Files', fontweight='bold')
        ax.set_title('File Count by Category', fontweight='bold', fontsize=12)
        ax.tick_params(axis='x', rotation=45)
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    def plot_size_bar(self, ax):
        if not self.category_size:
            ax.text(0.5, 0.5, 'No data available', 
                   ha='center', va='center', transform=ax.transAxes)
            ax.set_title('Storage Size by Category')
            return
        
        categories = list(self.category_size.keys())
        sizes_mb = [size / (1024 * 1024) for size in self.category_size.values()]
        
        colors = plt.cm.Spectral(range(len(categories)))
        bars = ax.barh(categories, sizes_mb, color=colors, edgecolor='black', linewidth=0.5)
        
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height()/2.,
                   f'{sizes_mb[i]:.1f} MB', ha='left', va='center', fontsize=9)
        
        ax.set_xlabel('Size (MB)', fontweight='bold')
        ax.set_ylabel('Category', fontweight='bold')
        ax.set_title(f'Storage Size by Category\nTotal: {self.format_size(self.total_size)}', 
                     fontweight='bold', fontsize=12)
    
    def plot_extension_bar(self, ax):
        if not self.extension_count:
            ax.text(0.5, 0.5, 'No data available', 
                   ha='center', va='center', transform=ax.transAxes)
            ax.set_title('Top File Extensions')
            return
        
      
        sorted_exts = sorted(self.extension_count.items(), 
                            key=lambda x: x[1], reverse=True)[:10]
        
        extensions = [ext if ext else '(no ext)' for ext, _ in sorted_exts]
        counts = [count for _, count in sorted_exts]
        
        colors = plt.cm.viridis(range(len(extensions)))
        bars = ax.bar(extensions, counts, color=colors, edgecolor='black', linewidth=0.5)
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}', ha='center', va='bottom', fontsize=9)
        
        ax.set_xlabel('File Extension', fontweight='bold')
        ax.set_ylabel('Count', fontweight='bold')
        ax.set_title('Top 10 File Extensions', fontweight='bold', fontsize=12)
        ax.tick_params(axis='x', rotation=45)
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    def format_size(self, size):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} PB"
