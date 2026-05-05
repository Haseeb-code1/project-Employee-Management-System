import os
import glob

# Update style.py for Treeview background
style_code = """import customtkinter as ctk

def setup_theme():
    ctk.set_appearance_mode('Dark')
    ctk.set_default_color_theme('blue')

def apply_treeview_style():
    from tkinter import ttk
    style = ttk.Style()
    style.theme_use('default')
    # Light blue background for the data table
    style.configure('Treeview', background='#add8e6', foreground='black', rowheight=30, fieldbackground='#add8e6', bordercolor='#343638', borderwidth=0)
    style.map('Treeview', background=[('selected', '#1f538d')], foreground=[('selected', 'white')])
    style.configure('Treeview.Heading', background='#1f538d', foreground='white', relief='flat', font=('Roboto', 10, 'bold'))
    style.map('Treeview.Heading', background=[('active', '#14375e')])
"""

with open('tkinter_app/app/utils/style.py', 'w') as f:
    f.write(style_code)

# Update all input fields to have light blue background
views_dir = 'tkinter_app/app/views'
for filepath in glob.glob(os.path.join(views_dir, '*.py')):
    with open(filepath, 'r') as f:
        content = f.read()
    
    if 'fg_color="#add8e6"' not in content:
        content = content.replace('ctk.CTkEntry(', 'ctk.CTkEntry(fg_color="#add8e6", text_color="black", placeholder_text_color="#444444", ')
        content = content.replace('ctk.CTkComboBox(', 'ctk.CTkComboBox(fg_color="#add8e6", text_color="black", ')
        
        with open(filepath, 'w') as f:
            f.write(content)

print('Updated UI colors.')
