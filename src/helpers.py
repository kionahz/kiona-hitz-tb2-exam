# clear all widgets to be able to open new page with new widgets
def clear_widgets(root):
    for i in root.winfo_children():
        i.destroy()
