import customtkinter as ctk

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
