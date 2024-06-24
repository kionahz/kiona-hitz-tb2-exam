def clear_widgets(root):
    for i in root.winfo_children():
        i.destroy()
