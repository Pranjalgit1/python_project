import json
import os

class ThemeManager:
    
    
    def __init__(self):
        self.themes = {
            'light': {
                'bg': '#f0f0f0',
                'fg': '#000000',
                'button_bg': '#e0e0e0',
                'button_fg': '#000000',
                'button_active_bg': '#d0d0d0',
                'entry_bg': '#ffffff',
                'entry_fg': '#000000',
                'listbox_bg': '#ffffff',
                'listbox_fg': '#000000',
                'label_bg': '#f0f0f0',
                'label_fg': '#000000',
                'frame_bg': '#f0f0f0',
                'accent': '#2196F3',
                'success': '#4CAF50',
                'error': '#f44336',
                'warning': '#FF9800'
            },
            'dark': {
                'bg': '#1e1e1e',
                'fg': '#ffffff',
                'button_bg': '#2d2d2d',
                'button_fg': '#ffffff',
                'button_active_bg': '#3d3d3d',
                'entry_bg': '#2d2d2d',
                'entry_fg': '#ffffff',
                'listbox_bg': '#2d2d2d',
                'listbox_fg': '#ffffff',
                'label_bg': '#1e1e1e',
                'label_fg': '#ffffff',
                'frame_bg': '#1e1e1e',
                'accent': '#64B5F6',
                'success': '#81C784',
                'error': '#E57373',
                'warning': '#FFB74D'
            }
        }
        
        self.current_theme = 'light'
        self.load_preference()
    
    def get_theme_file(self):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                           '.theme_preference.json')
    
    def load_preference(self):
        try:
            theme_file = self.get_theme_file()
            if os.path.exists(theme_file):
                with open(theme_file, 'r') as f:
                    data = json.load(f)
                    self.current_theme = data.get('theme', 'light')
        except:
            self.current_theme = 'light'
    
    def save_preference(self):
        try:
            theme_file = self.get_theme_file()
            with open(theme_file, 'w') as f:
                json.dump({'theme': self.current_theme}, f)
        except:
            pass
    
    def get_current_theme(self):
        return self.current_theme
    
    def get_colors(self):
        return self.themes[self.current_theme]
    
    def toggle_theme(self):
        self.current_theme = 'dark' if self.current_theme == 'light' else 'light'
        self.save_preference()
        return self.current_theme
    
    def set_theme(self, theme_name):
        if theme_name in self.themes:
            self.current_theme = theme_name
            self.save_preference()
            return True
        return False
    
    def apply_theme(self, widget, widget_type='default'):
        colors = self.get_colors()
        
        try:
            if widget_type == 'button':
                widget.config(
                    bg=colors['button_bg'],
                    fg=colors['button_fg'],
                    activebackground=colors['button_active_bg'],
                    activeforeground=colors['button_fg']
                )
            elif widget_type == 'entry':
                widget.config(
                    bg=colors['entry_bg'],
                    fg=colors['entry_fg'],
                    insertbackground=colors['fg']
                )
            elif widget_type == 'listbox':
                widget.config(
                    bg=colors['listbox_bg'],
                    fg=colors['listbox_fg']
                )
            elif widget_type == 'label':
                widget.config(
                    bg=colors['label_bg'],
                    fg=colors['label_fg']
                )
            elif widget_type == 'frame':
                widget.config(bg=colors['frame_bg'])
            else:
                widget.config(bg=colors['bg'], fg=colors['fg'])
        except:
            pass
    
    def apply_theme_to_window(self, window):
        colors = self.get_colors()
        window.config(bg=colors['bg'])
        
        self._apply_recursive(window, colors)
    
    def _apply_recursive(self, widget, colors):
        widget_class = widget.winfo_class()
        
        try:
            if widget_class == 'Button':
                widget.config(
                    bg=colors['button_bg'],
                    fg=colors['button_fg'],
                    activebackground=colors['button_active_bg'],
                    activeforeground=colors['button_fg']
                )
            elif widget_class == 'Entry':
                widget.config(
                    bg=colors['entry_bg'],
                    fg=colors['entry_fg'],
                    insertbackground=colors['fg']
                )
            elif widget_class == 'Listbox':
                widget.config(
                    bg=colors['listbox_bg'],
                    fg=colors['listbox_fg']
                )
            elif widget_class == 'Label':
                widget.config(
                    bg=colors['label_bg'],
                    fg=colors['label_fg']
                )
            elif widget_class in ['Frame', 'Toplevel']:
                widget.config(bg=colors['frame_bg'])
            elif widget_class == 'Text':
                widget.config(
                    bg=colors['entry_bg'],
                    fg=colors['entry_fg'],
                    insertbackground=colors['fg']
                )
        except:
            pass
        
        # Apply to children
        for child in widget.winfo_children():
            self._apply_recursive(child, colors)
