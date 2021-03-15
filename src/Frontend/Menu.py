import tkinter as tk
from tkinter.filedialog import asksaveasfile
from tkinter import *

from src.DemoStuff import DemoStuff
from src.Backend.District import *

from PIL import Image
from PIL import ImageTk


class ResizingCanvas(tk.Canvas):
    """
    This altered Canvas stores the current size and acts like a normal canvas.
    It also includes the trigger for scaling the map when resizing the window.

    Methods
    -------
    resize(self, event)
        Handles the action of resizing the window appropriately
    """

    def __init__(self, parent, **kwargs):
        tk.Canvas.__init__(self, parent, **kwargs)
        self.bind("<Configure>", self.resize)
        self.height = self.winfo_height()
        self.width = self.winfo_width()
        self.permheight = self.winfo_height()
        self.permwidth = self.winfo_width()

    def resize(self, event):
        """
        Takes in the Canvas and the event and resizes the contents of the map accordingly.
        *Not Perfect, needs some work*

        Parameters
        ----------
        self: Modified Canvas

        event: the resizing of the window
        """
        wscale = float(event.width) / self.width
        hscale = float(event.height) / self.height
        self.width = event.width
        self.height = event.height
        if self.width > 300 or self.height > 250:
            if self.height < self.width:
                self.scale("all", 0, 0, hscale, hscale)
            else:
                self.scale("all", 0, 0, wscale, wscale)
        else:
            print("THings")
            wscale = float(event.width) / self.permwidth
            hscale = float(event.height) / self.permheight
            self.scale("all", 0, 0, wscale, hscale)
        return


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
        0 = Farmland - Green
        1 = Housing - Sandy Orangy
        2 = Docks - Dark Blue
        3 = Smithing - Black
        4 = Slum - Brown
        5 = Market - Teal
        6 = Castle - Grey
        7 = Cathedral - Purple
        8 = Armory - Pale Red
        9 = Warcamp - Light Limy Green
        10 = Gate - Tan/Gray Wall Paint like
        11 = Precinct - Yellow
        12 = Building - Black
        """

        # https://www.colorcombos.com/combotester.html?color0=4aa75d&color1=ffac58&color2=003399&color3=020101&color4=ac6024&color5=6ab0b0&color6=a3a3a3&color7=952e85&color8=a93939&color9=7ba74c&color10=e5e5be&color11=eaea02&show_text=
        switcher = {
            0: "#4aa75d",  # Green
            1: "#ffac58",  # Sandy Orangy
            2: "#003399",  # Dark Blue
            3: "#020101",  # Black
            4: "#ac6024",  # Brown
            5: "#6ab0b0",  # Teal
            6: "#a3a3a3",  # Grey
            7: "#952e85",  # Purple
            8: "#a93939",  # Pale Red
            9: "#7ba74c",  # Light Limy Green
            10: "#e5e5be",  # Tan/Gray Wall Paint like
            11: "#eaea02",  # Yellow
            12: "#000000"  # Black - Building
        }
        map_canvas.create_polygon(*points, fill=switcher.get(region_type, "#ebd5b3"))

    def draw_map(map_canvas):
        map_canvas.delete("all")
        reg_list = DemoStuff().assign_districts()
        switch_val = 0
        for reg in reg_list:
            dis = reg.get_district()
            if isinstance(dis, Farmland):
                switch_val = 0
            if isinstance(dis, Housing):
                switch_val = 1
            if isinstance(dis, Docks):
                switch_val = 2
            if isinstance(dis, Smithing):
                switch_val = 3
            if isinstance(dis, Slum):
                switch_val = 4
            if isinstance(dis, Market):
                switch_val = 5
            if isinstance(dis, Castle):
                switch_val = 6
            if isinstance(dis, Cathedral):
                switch_val = 7
            if isinstance(dis, Armory):
                switch_val = 8
            if isinstance(dis, WarCamp):
                switch_val = 9
            if isinstance(dis, Gate):
                switch_val = 10
            if isinstance(dis, Precinct):
                switch_val = 11
            verts = []
            for v in reg.get_vertices():
                verts.append((v.get_x() + 900)/7.5)
                verts.append((v.get_y() + 400)/7.5)
            draw_region(map_canvas, switch_val, verts)
            for build in reg.buildings:
                verts = []
                for v in build.get_vertices():
                    verts.append((v.get_x() + 900)/7.5)
                    verts.append((v.get_y() + 400)/7.5)
                draw_region(map_canvas, 12, verts)

    def help_msg():
        """
        command for the help message
        """
        info = Toplevel()
        info.title('Help Window')
        info.iconbitmap('../../images/Atlas.ico')
        Label(info, text="ATLAS help", font="Helvetica 16 bold", bg="#a3a3a3").pack(side=TOP)
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
    window.minsize(300, 250)

    # creates the welcome window
    welcome = tk.Toplevel(window)
    welcome.title('Welcome Window')
    Label(welcome, text="Welcome to ATLAS", font="Helvetica 16 bold", bg="#a3a3a3").pack(side=TOP)
    Label(welcome, text="Hello user, thank you for downloading our map generator.\n").pack(side=TOP)
    Label(welcome, text=" Directions:\n\n\n").pack(side=LEFT)
    Label(welcome, text="To create the map click generate.").pack()
    Label(welcome, text="To create the map click generate.").pack()
    Button(welcome, text="Close", command=welcome.destroy).pack(side=BOTTOM)

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
    button_frame.rowconfigure(4, weight=2)

    # Create the canvas that the picture will be rendered on
    canvas = ResizingCanvas(window, background="#ebd5b3")
    canvas.grid(column=1, row=0, sticky=('n', 's', 'e', 'w'))

    # Each of These are for the buttons that are created
    action_btn = tk.Button(button_frame, text="Generate", background="#6ab0b0", foreground="black",
                           command=lambda: draw_map(canvas))  # Replace this with draw_map when I have it made
    action_btn.grid(column=0, row=0, sticky='w', padx=5, pady=5)

    load_btn = tk.Button(button_frame, text="Load", background="#ac6024", foreground="black")
    load_btn.grid(column=0, row=1, sticky='w', padx=5)

    save_btn = tk.Button(button_frame, text="Save", background="#4aa75d", foreground="black",
                         command=lambda: save_file())
    save_btn.grid(column=0, row=2, sticky='w', padx=5, pady=5)

    help_btn = tk.Button(button_frame, text="Help", background="#a3a3a3", foreground="black", command=help_msg)
    help_btn.grid(column=0, row=3, sticky='w', padx=5)

    # Sets up and puts the image of the cardinal directions on the screen 
    img = tk.PhotoImage(file='../../images/compass.png')
    mylabel = tk.Label(button_frame, image=img, background="#CCCCCC")
    mylabel.grid(column=0, row=4, sticky='s', padx=10, pady=10)

    window.mainloop()


if __name__ == '__main__':
    main()
