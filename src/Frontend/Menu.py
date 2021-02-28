import tkinter as tk
from tkinter.filedialog import asksaveasfile
from tkinter import *


def main():
    
    def draw_region(map_canvas, region_type, points):
        """
        command to draw a region as specified on the map,
        Will handle populating each region according to type

        Parameters
        ----------
        map_canvas : Canvas
            The canvas that the region will be displayed on
        region_type : Integer
            Corresponds to the type of region on the map
        points : Integer Array
            An array of points for making a polygon, not as tuples, (x1, y1, x2, y2,...)

        Region encoding:
        0 = Farmland
        1 = Housing
        2 = Docks
        3 = Smithing
        4 = Slum
        5 = Market
        6 = Castle
        -Up For Debate Colors (Especially if these aren't actual areas, I just went off of the defined regions)-
        7 = Cathedral
        8 = Armory
        9 = Warcamp
        10 = Gate
        11 = Precinct
        """
        switcher = {
            0: "#4aa75d",
            1: "#ffac58",
            2: "#003399",
            3: "#020101",
            4: "#ac6024",
            5: "#6ab0b0",
            6: "#a3a3a3",
            7: "#952e85",
            8: "#a93939",
            9: "#7ba74c",
            10: "#e5e5be",
            11: "#dadabc"
        }
        map_canvas.create_polygon(*points, fill=switcher.get(region_type, "#ebd5b3"))

    def help_msg():
        """
        command for the help message
        """
        info = Toplevel()
        info.title('Help Window')
        info.iconbitmap('../../images/Atlas.ico')
        Label(info, text="This is filler text till I know what to write here").pack()
        Button(info, text="Close", command=info.destroy).pack()

    def save_file():
        """
        sets up ability to save
        """
        files = [('All Files', '*.*'),
                 ('PNG', '*.png'),
                 ('Text Document', '*.txt')]
        file = asksaveasfile(filetypes=files, defaultextension=files)
        if not files:
            return

    # create the window object
    window = tk.Tk()
    window.title("Atlas")

    # creates the welcome window
    welcome = tk.Toplevel(window)
    welcome.title('Welcome Window')
    Label(welcome, text="Hello user, thank you for downloading our map generator.").pack()
    Button(welcome, text="Close", command=welcome.destroy).pack()

    # sets the icons in the corner to our logo
    window.iconbitmap('../../images/Atlas.ico')
    welcome.iconbitmap('../../images/Atlas.ico')

    # configure the two columns to expand properly
    window.columnconfigure(0, weight=0)
    window.columnconfigure(1, weight=1)
    window.rowconfigure(0, weight=1)

    # Creates the button frame
    button_frame = tk.Frame(background="#CCCCCC", relief='raised', width=8)
    button_frame.grid(column=0, row=0, sticky=('n', 's', 'e', 'w'))

    # Create the canvas that the picture will be rendered on
    canvas = tk.Canvas(background="#ebd5b3")
    canvas.grid(column=1, row=0, sticky=('n', 's', 'e', 'w'))

    # Each of These are for the buttons that are created
    action_btn = tk.Button(button_frame, text="Generate", background="#6ab0b0", foreground="black",
                           command=lambda: draw_region(canvas, 9, [100, 150, 50, 50, 200, 50, 200,
                                                                   150, 300, 450, 275, 500]))  # Replace this with draw_map when I have it made
    action_btn.grid(column=0, row=0, sticky='w', padx=5, pady=5)

    load_btn = tk.Button(button_frame, text="Load", background="#ac6024", foreground="black")
    load_btn.grid(column=0, row=1, sticky='w', padx=5)

    save_btn = tk.Button(button_frame, text="Save", background="#4aa75d", foreground="black",
                         command=lambda: save_file())
    save_btn.grid(column=0, row=2, sticky='w', padx=5, pady=5)

    help_btn = tk.Button(button_frame, text="Help", background="#a3a3a3", foreground="black", command=help_msg)
    help_btn.grid(column=0, row=3, sticky='w', padx=5)

    window.mainloop()


if __name__ == '__main__':
    main()
