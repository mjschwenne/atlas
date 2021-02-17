import tkinter as tk

# create the window object
window = tk.Tk()

title = window.title("Atlas")

# configure the two columns to expand properly
window.columnconfigure(0, weight=0)
window.columnconfigure(1, weight=1)
window.rowconfigure(0, weight=1)

# Creates the button frame
button_frame = tk.Frame(background="#c9c9b3", relief='raised', width=8)
button_frame.grid(column=0, row=0, sticky=('n', 's', 'e', 'w'))

# Each of These are for the buttons that are created
action_btn = tk.Button(button_frame, text="Generate", background="black", foreground="white")
action_btn.grid(column=0, row=0, sticky='w', padx=5, pady=5)

load_btn = tk.Button(button_frame, text="Load", background="yellow", foreground="black")
load_btn.grid(column=0, row=1, sticky='w', padx=5)

save_btn = tk.Button(button_frame, text="Save", background="green", foreground="white")
save_btn.grid(column=0, row=2, sticky='w', padx=5, pady=5)

help_btn = tk.Button(button_frame, text="Help", background="red", foreground="white")
help_btn.grid(column=0, row=3, sticky='w', padx=5)

# Create the canvas that the picture will be rendered on
canvas = tk.Canvas(background="#e3df5f")
canvas.grid(column=1, row=0, sticky=('n', 's', 'e', 'w'))

window.mainloop()
