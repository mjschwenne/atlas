import tkinter as tk
from tkinter.filedialog import asksaveasfile
from tkinter import *

from src.Backend.Constructor import Constructor
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
        1 = HousingMid - Sandy Orangy
        2 = HousingLow - Dark Blue
        3 = HousingHigh - Black
        4 = Slum - Brown
        5 = Market - Teal
        6 = Castle - Grey
        7 = Cathedral - Purple
        8 = Armory - Pale Red
        9 = Shops - Light Limy Green
        10 = Gate - Tan/Gray Wall Paint like
        11 = Precinct - Yellow
        12 = Building - White
        13 = Industrial - Pink
        14 = Openland - Light Purple
        15 = Courtyard - Dark Blue
        16 = Park - Dark Green
        """

        # https://www.colorcombos.com/combotester.html?color0=4aa75d&color1=ffac58&color2=003399&color3=020101&color4=ac6024&color5=6ab0b0&color6=a3a3a3&color7=952e85&color8=a93939&color9=7ba74c&color10=e5e5be&color11=eaea02&show_text=
        switcher = {
            0: "#4aa75d",  # Green
            1: "#ffac58",  # Sandy Orangy
            2: "#003399",  # Blue
            3: "#020101",  # Black
            4: "#ac6024",  # Brown
            5: "#6ab0b0",  # Teal
            6: "#a3a3a3",  # Grey
            7: "#952e85",  # Purple
            8: "#a93939",  # Pale Red
            9: "#7ba74c",  # Light Limy Green
            10: "#e5e5be",  # Tan/Gray Wall Paint like
            11: "#eaea02",  # Yellow
            12: "#FFFFFF",  # Black - Building
            13: "#fc2fff",  # Pink - Industrial
            14: "#a192fb",  # Light Purple - Openland
            15: "#003378",  # Dark Blue - Courtyard
            16: "#046113"  # Dark Green - Park
        }
        map_canvas.create_polygon(*points, fill=switcher.get(region_type, "#ebd5b3"))

    def draw_map(map_canvas):
        map_canvas.delete("all")
        reg_list = Constructor().generate_map()
        switch_val = 0
        for reg in reg_list:
            dis = reg.get_district()
            if isinstance(dis, Farmland):
                switch_val = 0
            if isinstance(dis, HousingMid):
                switch_val = 1
            if isinstance(dis, HousingLow):
                switch_val = 2
            if isinstance(dis, HousingHigh):
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
            if isinstance(dis, Shops):
                switch_val = 9
            if isinstance(dis, Gate):
                switch_val = 10
            if isinstance(dis, Precinct):
                switch_val = 11
            if isinstance(dis, Industrial):
                switch_val = 13
            if isinstance(dis, Openland):
                switch_val = 14
            if isinstance(dis, Courtyard):
                switch_val = 15
            if isinstance(dis, Park):
                switch_val = 16
            verts = []
            for v in reg.get_vertices():
                verts.append((v.get_x() + 250) / 2)
                verts.append((v.get_y() + 250) / 2)
            draw_region(map_canvas, switch_val, verts)
            for build in reg.buildings:
                verts = []
                for v in build.get_vertices():
                    verts.append((v.get_x() + 250) / 2)
                    verts.append((v.get_y() + 250) / 2)
                draw_region(map_canvas, 12, verts)

    def help_msg():
        """
        command for the help message
        """
        info = Toplevel()
        info.title('Help Window')
        info.iconbitmap('../../images/Atlas.ico')
        Label(info, text="ATLAS Help Window", font="Helvetica 16 bold", bg="#a3a3a3").pack(side=TOP)
        Label(info, text="This is filler text till I know what to write here").pack()
        Button(info, text="Close", command=info.destroy).pack()

    def edit_msg():
        """
        command for the help message
        """
        edit = Toplevel()
        edit.title('Edit Window')
        edit.geometry('250x700')
        edit.iconbitmap('../../images/Atlas.ico')
        edit.rowconfigure(25, weight=2)

        def var_states():
            print("N 10:%d,\n25:%d,\n50:%d,\n75:%d,\n100:%d" % (var1.get(), var2.get(), var3.get(), var4.get(),
                                                                var5.get()))
            print("T Armory:%d,\nBuilding:%d,\nCastle:%d,\nCathedral:%d,\nCourtyard:%d,\nFarmland:%d,\nGate:%d,"
                  "\nHousingHigh:%d,\nHousingLow:%d,\nHousingMid:%d,\nIndustrial:%d,\nMarket:%d,\nOpenland:%d,"
                  "\nPark:%d,\nPrecinct:%d,\nShops:%d,\nSlum:%d" % (var6.get(), var7.get(), var8.get(), var9.get(),
                                                                    var10.get(), var11.get(), var12.get(), var13.get(),
                                                                    var14.get(), var15.get(), var16.get(),
                                                                    var17.get(), var18.get(), var19.get(), var20.get(),
                                                                    var21.get(), var22.get()))
            
        Label(edit, text="How Many Districts?", font="Helvetica 16 bold", bg="#a3a3a3").grid(row=0, sticky=W)
        var1 = IntVar()
        Checkbutton(edit, text="10", variable=var1).grid(row=1, sticky=W)
        var2 = IntVar()
        Checkbutton(edit, text="25", variable=var2).grid(row=2, sticky=W)
        var3 = IntVar()
        Checkbutton(edit, text="50", variable=var3).grid(row=3, sticky=W)
        var4 = IntVar()
        Checkbutton(edit, text="75", variable=var4).grid(row=4, sticky=W)
        var5 = IntVar()
        Checkbutton(edit, text="100", variable=var5).grid(row=5, sticky=W)

        Label(edit, text="What Type of Districts?", font="Helvetica 16 bold", bg="#a3a3a3").grid(row=6, sticky=W)
        var6 = IntVar()
        Checkbutton(edit, text="Armory", variable=var6).grid(row=7, sticky=W)
        var7 = IntVar()
        Checkbutton(edit, text="Building", variable=var7).grid(row=8, sticky=W)
        var8 = IntVar()
        Checkbutton(edit, text="Castle", variable=var8).grid(row=9, sticky=W)
        var9 = IntVar()
        Checkbutton(edit, text="Cathedral", variable=var9).grid(row=10, sticky=W)
        var10 = IntVar()
        Checkbutton(edit, text="Courtyard", variable=var10).grid(row=11, sticky=W)
        var11 = IntVar()
        Checkbutton(edit, text="Farmland", variable=var11).grid(row=12, sticky=W)
        var12 = IntVar()
        Checkbutton(edit, text="Gate", variable=var12).grid(row=13, sticky=W)
        var13 = IntVar()
        Checkbutton(edit, text="Housing High ", variable=var13).grid(row=14, sticky=W)
        var14 = IntVar()
        Checkbutton(edit, text="Housing Low", variable=var14).grid(row=15, sticky=W)
        var15 = IntVar()
        Checkbutton(edit, text="Housing Mid", variable=var15).grid(row=16, sticky=W)
        var16 = IntVar()
        Checkbutton(edit, text="Industrial", variable=var16).grid(row=17, sticky=W)
        var17 = IntVar()
        Checkbutton(edit, text="Market", variable=var17).grid(row=18, sticky=W)
        var18 = IntVar()
        Checkbutton(edit, text="Open Land", variable=var18).grid(row=19, sticky=W)
        var19 = IntVar()
        Checkbutton(edit, text="Park", variable=var19).grid(row=20, sticky=W)
        var20 = IntVar()
        Checkbutton(edit, text="Precinct", variable=var20).grid(row=21, sticky=W)
        var21 = IntVar()
        Checkbutton(edit, text="Shops", variable=var21).grid(row=22, sticky=W)
        var22 = IntVar()
        Checkbutton(edit, text="Slums", variable=var22).grid(row=23, sticky=W)

        Button(edit, text='Go', command=var_states).grid(row=25, sticky=W, pady=4, padx=4)
        Button(edit, text='Quit', command=edit.destroy).grid(row=25, sticky=E, pady=4, padx=4)

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
    button_frame.rowconfigure(5, weight=2)

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

    edit_btn = tk.Button(button_frame, text="Edit", background="#a3a3a3", foreground="black", command=edit_msg)
    edit_btn.grid(column=0, row=3, sticky='w', padx=5, pady=5)

    help_btn = tk.Button(button_frame, text="Help", background="#a3a3a3", foreground="black", command=help_msg)
    help_btn.grid(column=0, row=4, sticky='w', padx=5, pady=5)

    # Sets up and puts the image of the cardinal directions on the screen 
    img = tk.PhotoImage(file='../../images/compass.png')
    mylabel = tk.Label(button_frame, image=img, background="#CCCCCC")
    mylabel.grid(column=0, row=5, sticky='s', padx=10, pady=10)

    window.mainloop()


if __name__ == '__main__':
    main()
