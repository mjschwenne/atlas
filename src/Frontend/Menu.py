import tkinter
import tkinter as tk
import tkinter.messagebox
from tkinter.filedialog import asksaveasfilename, asksaveasfile


def help_msg():
    tkinter.messagebox.showinfo("Having trouble", "All you need to do is click generate")


def save_file():
    files = [('All Files', '*.*'),
             ('PNG', '*.png'),
             ('Text Document', '*.txt')]
    file = asksaveasfile(filetypes=files, defaultextension=files)
    if not files:
        return


def main():
    # create the window object
    window = tk.Tk()

    title = window.title("Atlas")

    # configure the two columns to expand properly
    window.columnconfigure(0, weight=0)
    window.columnconfigure(1, weight=1)
    window.rowconfigure(0, weight=1)

    # Creates the button frame
    button_frame = tk.Frame(background="#CCCCCC", relief='raised', width=8)
    button_frame.grid(column=0, row=0, sticky=('n', 's', 'e', 'w'))

    # Each of These are for the buttons that are created
    action_btn = tk.Button(button_frame, text="Generate", background="#6ab0b0", foreground="black")
    action_btn.grid(column=0, row=0, sticky='w', padx=5, pady=5)

    load_btn = tk.Button(button_frame, text="Load", background="#ac6024", foreground="black")
    load_btn.grid(column=0, row=1, sticky='w', padx=5)

    save_btn = tk.Button(button_frame, text="Save", background="#4aa75d", foreground="black",
                         command=lambda: save_file())
    save_btn.grid(column=0, row=2, sticky='w', padx=5, pady=5)

    help_btn = tk.Button(button_frame, text="Help", background="#a3a3a3", foreground="black", command=help_msg)
    help_btn.grid(column=0, row=3, sticky='w', padx=5)

    # Create the canvas that the picture will be rendered on
    canvas = tk.Canvas(background="#ebd5b3")
    canvas.grid(column=1, row=0, sticky=('n', 's', 'e', 'w'))

    window.mainloop()


if __name__ == '__main__':
    main()
