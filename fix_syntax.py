import os
import glob
import re

views_dir = 'tkinter_app/app/views'
for filepath in glob.glob(os.path.join(views_dir, '*.py')):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # 1. Remove the broken arguments from the beginning
    content = content.replace('fg_color="#add8e6", text_color="black", placeholder_text_color="#444444", ', '')
    content = content.replace('fg_color="#add8e6", text_color="black", ', '')

    # 2. Add them safely at the end of the parameters
    content = re.sub(r'ctk\.CTkEntry\(([^,]+),', r'ctk.CTkEntry(\1, fg_color="#add8e6", text_color="black", placeholder_text_color="#444444",', content)
    content = re.sub(r'ctk\.CTkComboBox\(([^,]+),', r'ctk.CTkComboBox(\1, fg_color="#add8e6", text_color="black",', content)

    with open(filepath, 'w') as f:
        f.write(content)

print('Fixed syntax errors in UI files.')
