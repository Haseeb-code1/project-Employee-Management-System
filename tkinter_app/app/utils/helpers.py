import tkinter.messagebox as messagebox

def show_error(title, message):
    messagebox.showerror(title, message)

def show_info(title, message):
    messagebox.showinfo(title, message)

def confirm_action(title, message):
    return messagebox.askyesno(title, message)
