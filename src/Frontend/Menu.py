import tkinter as tk
import tkinter as ttk
from tkinter.filedialog import asksaveasfilename
from tkinter import *
from PIL import ImageGrab, Image
import os

from src.Backend.Constructor import Constructor
from src.Backend.District import *

user_info = [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
customize_info = [0, 1]
map_regions = []


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
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()
        self.permheight = self.winfo_reqheight()
        self.permwidth = self.winfo_reqwidth()
        self.text_height = 2

    def resize(self, event):
        """
        Takes in the Canvas and the event and resizes the contents of the map accordingly.
        *Not Perfect, needs some work*

        Parameters
        ----------
        self: Modified Canvas

        event: the resizing of the window
        """

        # determine the ratio of old width/height to new width/height
        wscale = event.width / self.width
        hscale = event.height / self.height
        self.width = event.width
        self.height = event.height
        # rescale all the objects
        self.scale("all", 0, 0, wscale, hscale)
        # font = self.itemcget("text", "font").split()
        self.text_height = self.text_height * wscale
        self.itemconfigure("text", font=("TkTextFont", round(self.text_height)))
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
        map_canvas.create_polygon(*points, fill=switcher.get(region_type, "#ebd5b3"), outline='black')

    def draw_walls(map_canvas, verts):
        length = len(verts)
        for i in len(verts):
            if i % 2 == 0:
                map_canvas.create_line(verts[i], verts[(i + 1) % length], verts[(i + 2) % length],
                                       verts[(i + 3) % length], width=8, color="#7B7F85")

        for i in len(verts):
            if i % 2 == 0:
                map_canvas.create_oval(verts[i] - 4, verts[i + 1] - 4, verts[i] + 4, verts[i + 1] + 4, color="#7B7F85")

    def find_map_bounds(verts):
        """
        This function is used by the draw_map function to locate the bounds of the map for use in scaling and sizing
        :param verts: An array of vertices for all polygons to be drawn
        :return: The highest and lowest values of each axis
        """
        i = 0
        lowest_width = float('inf')
        highest_width = float('-inf')
        lowest_height = float('inf')
        highest_height = float('-inf')
        for i in range(len(verts)):
            if i % 2 == 0:
                # check for highest /lowest width
                if verts[i] < lowest_width:
                    lowest_width = verts[i]
                if verts[i] > highest_width:
                    highest_width = verts[i]
            else:
                # check for highest / lowest height
                if verts[i] < lowest_height:
                    lowest_height = verts[i]
                if verts[i] > highest_height:
                    highest_height = verts[i]
        return lowest_width, highest_width, lowest_height, highest_height

    def select_random_name(string):
        final_string = string
        try:
            file = open("names/" + string + ".txt", "r")
            lines = file.readlines()
            chosen_line = random.randint(0, len(lines) - 1)
        except OSError as err:
            return final_string
        except ValueError:
            return final_string
        if lines[chosen_line] is None:
            file.close()
            return final_string
        else:
            final_string = lines[chosen_line]
            file.close()
        return final_string

    def label_regions(map_canvas, center_verts, string, color):
        """

        :param map_canvas:
        :param verts:
        :param string:
        :param color:
        :return:
        """
        i = 0
        for i in range(len(center_verts)):
            if i % 2 == 0:
                map_regions.append(select_random_name(string[int(i / 2)]))
                map_canvas.create_rectangle(center_verts[i] - 2, center_verts[i + 1] - 2, center_verts[i] + 2,
                                            center_verts[i + 1] + 2, fill="#ebd5b3", tags='label')
                map_canvas.create_text(center_verts[i], center_verts[i + 1], text=int(i / 2) + 1
                                       , font=("TkTextFont", int(map_canvas.text_height)), fill=color[int(i / 2)],
                                       tags=('text', 'label'), anchor=tk.CENTER)
        return

    def draw_map(map_canvas):
        """
        This function takes the generated points and sorts them into each group and draws them on the canvas
        :param map_canvas: The canvas to be drawn on
        :return: null
        """
        map_regions.clear()
        map_canvas.delete("all")
        construct = Constructor(None)
        reg_list = construct.generate_map(user_info)
        wall = construct.wall

        verts = []
        center_verts = []
        for reg in reg_list:
            center_verts.append(reg.get_center().get_x() + 250 / 2)
            center_verts.append(reg.get_center().get_y() + 250 / 2)
            for v in reg.get_vertices():
                verts.append((v.get_x() + 250) / 2)
                verts.append((v.get_y() + 250) / 2)
        low_w, high_w, low_h, high_h = find_map_bounds(verts)
        w = math.ceil(high_w - low_w)
        h = math.ceil(high_h - low_h)

        switch_val = 0
        string = []
        color = []
        for reg in reg_list:
            dis = reg.get_district()
            if isinstance(dis, Farmland):
                switch_val = 0
                string.append("Farmland")
                color.append('black')
            if isinstance(dis, HousingMid):
                switch_val = 1
                string.append("Housing")
                color.append('black')
            if isinstance(dis, HousingLow):
                switch_val = 2
                string.append("Housing")
                color.append('black')
            if isinstance(dis, HousingHigh):
                switch_val = 3
                string.append("Housing")
                color.append('black')
            if isinstance(dis, Slum):
                switch_val = 4
                string.append("Slums")
                color.append('black')
            if isinstance(dis, Market):
                switch_val = 5
                string.append("Market")
                color.append('black')
            if isinstance(dis, Castle):
                switch_val = 6
                string.append("Castle")
                color.append('black')
            if isinstance(dis, Cathedral):
                switch_val = 7
                string.append("Cathedral")
                color.append('black')
            if isinstance(dis, Armory):
                switch_val = 8
                string.append("Armory")
                color.append('black')
            if isinstance(dis, Shops):
                switch_val = 9
                string.append("Shops")
                color.append('black')
            if isinstance(dis, Gate):
                switch_val = 10
                string.append("Gate")
                color.append('black')
            if isinstance(dis, Precinct):
                switch_val = 11
                string.append("Precinct")
                color.append('black')
            if isinstance(dis, Industrial):
                switch_val = 13
                string.append("Industrial")
                color.append('black')
            if isinstance(dis, Openland):
                switch_val = 14
                string.append("Open")
                color.append('black')
            if isinstance(dis, Courtyard):
                switch_val = 15
                string.append("Courtyard")
                color.append('black')
            if isinstance(dis, Park):
                switch_val = 16
                string.append("Park")
                color.append('black')
            verts = []
            for v in reg.get_vertices():
                verts.append(((v.get_x() + 250) / 2) - low_w)
                verts.append(((v.get_y() + 250) / 2) - low_h)
            draw_region(map_canvas, switch_val, verts)
            for build in reg.buildings:
                verts = []
                for v in build.get_vertices():
                    verts.append(((v.get_x() + 250) / 2) - low_w)
                    verts.append(((v.get_y() + 250) / 2) - low_h)
                draw_region(map_canvas, 12, verts)
        wall_verts = []
        for verts in wall:
            wall_verts.append(((verts.get_x() + 250) / 2) - low_w)
            wall_verts.append(((verts.get_y() + 250) / 2) - low_w)
        draw_walls(map_canvas, wall_verts)

        center_verts = []
        for reg in reg_list:
            center_verts.append(((reg.get_center().get_x() + 250) / 2) - low_w)
            center_verts.append(((reg.get_center().get_y() + 250) / 2) - low_h)
        label_regions(map_canvas, center_verts, string, color)
        map_canvas.scale("all", 0, 0, map_canvas.width / w, map_canvas.height / h)
        return

    def help_msg():
        """
        command for the help message
        """
        info = Toplevel()
        info.title('Help Window')
        info.iconbitmap('../../images/Atlas.ico')
        Label(info, text="ATLAS Help Window", font="Helvetica 16 bold", bg="#a3a3a3", width=32).grid(row=0)
        Label(info, text="If you want a Randomly generated map hit the GENERATE button.\n "
                         "If you want to personalize what happens in the map hit the EDIT button.\n "
                         "If you want to save hit the SAVE button.").grid(row=1, sticky=W)
        Button(info, text="Close", command=info.destroy).grid(row=10)

    def key_msg():
        """
        command for the key
        """
        key = Toplevel()
        key.title('KEY')
        key.geometry('400x400')
        key.iconbitmap('../../images/Atlas.ico')
        Label(key, text="ATLAS District Key", font="Helvetica 16 bold", bg="#a3a3a3").pack(side=TOP)
        scrollbar = Scrollbar(key)
        scrollbar.pack(side=RIGHT, fill='y')
        region_list = Listbox(key, yscrollcommand=scrollbar.set)
        region_list.pack(side=LEFT, fill=BOTH, expand=1, padx=5, pady=5)
        scrollbar.config(command=region_list.yview)
        if not map_regions:
            region_list.insert(END, "No Map has been Generated")
        else:
            i = 0
            for name in map_regions:
                i += 1
                region_list.insert(END, str(i) + ". " + name)

    def edit_msg():
        """
        command for the edit window
        """
        edit = Toplevel()
        edit.title('Edit Window')
        edit.iconbitmap('../../images/Atlas.ico')
        edit.rowconfigure(25, weight=2)

        def var_states():
            """
            handles the printing of the edited

            Var Ordering:
            var1  = number of districts
                1 = 10
                2 = 25
                3 = 50
                4 = 75
                5 = 100
            var6  = Armory
            var7  = Building
            var8  = Castle
            var9  = Cathedral
            var10 = Courtyard
            var11 = Farmland
            var12 = Gate
            var13 = Housing High
            var14 = Housing Low
            var15 = Housing Mid
            var16 = Industrial
            var17 = Market
            var18 = Open land
            var19 = Park
            var20 = Precinct
            var21 = Shops
            var22 = Slum
            """

            global user_info
            # Makes the array for the use of deciding what districts the user wants in the map
            user_info = (var1.get(), var6.get(), var3.get(), var8.get(),
                         var9.get(), var10.get(), var11.get(), var12.get(),
                         var13.get(), var14.get(), var15.get(), var16.get(),
                         var17.get(), var18.get(), var19.get(), var20.get(),
                         var21.get(), var22.get())

            global customize_info
            # Makes the array for the use of deciding what custom information the user wants in the map
            customize_info = (var4, var5)

        # Handles the directions and seperateing the words between the 2 columns
        Label(edit, text="Directions", font="Helvetica 16 bold", bg="#a3a3a3").grid(column=0, row=0, sticky=E)
        Label(edit, text=":", font="Helvetica 16 bold", bg="#a3a3a3").grid(column=1, row=0, sticky=W)

        Label(edit, text="To generate your own map").grid(column=0, row=1, sticky=E)
        Label(edit, text="select how many districts.").grid(column=1, row=1, sticky=W)
        Label(edit, text="Then select what types of").grid(column=0, row=3, sticky=E)
        Label(edit, text="districts you what on your map.").grid(column=1, row=3, sticky=W)
        Label(edit, text="If you put a checkmark in the").grid(column=0, row=4, sticky=E)
        Label(edit, text="box it will be included in the map.").grid(column=1, row=4, sticky=W)

        Label(edit, text="After you have made your").grid(column=0, row=5, sticky=E)
        Label(edit, text="selections hit the GO button.").grid(column=1, row=5, sticky=W)
        Label(edit, text="If you want to reset to original").grid(column=0, row=6, sticky=E)
        Label(edit, text="settings hit the RESET button.").grid(column=1, row=6, sticky=W)
        Label(edit, text="If you want to exit").grid(column=0, row=7, sticky=E)
        Label(edit, text="hit the QUIT button.").grid(column=1, row=7, sticky=W)

        # Handles the first question in edit window and sets a variable to it
        Label(edit, text="How Many", font="Helvetica 16 bold", bg="#a3a3a3").grid(column=0, row=8, sticky=E)
        Label(edit, text="Districts?", font="Helvetica 16 bold", bg="#a3a3a3").grid(column=1, row=8, sticky=W)
        var1 = IntVar()
        Checkbutton(edit, text="10  ", font="Helvetica 10", variable=var1, onvalue=1).grid(row=9, sticky=E)
        Checkbutton(edit, text="25  ", font="Helvetica 10", variable=var1, onvalue=2).grid(row=10, sticky=E)
        Checkbutton(edit, text="50  ", font="Helvetica 10", variable=var1, onvalue=3).grid(row=11, sticky=E)
        Checkbutton(edit, text="75  ", font="Helvetica 10", variable=var1, onvalue=4).grid(row=12, sticky=E)
        Checkbutton(edit, text="100", font="Helvetica 10", variable=var1, onvalue=5).grid(row=13, sticky=E)

        # Handles second question and variables for each of the options
        Label(edit, text="Buildings", font="Helvetica 16 bold", bg="#a3a3a3").grid(column=0, row=14, sticky=E)
        Label(edit, text="and Visuals", font="Helvetica 16 bold", bg="#a3a3a3").grid(column=1, row=14, sticky=W)
        var3 = IntVar()
        Checkbutton(edit, text="Buildings   ", font="Helvetica 10", variable=var3).grid(row=15, sticky=W)
        var4 = IntVar()
        Checkbutton(edit, text="Grey Scale", font="Helvetica 10", variable=var4).grid(row=16, sticky=W)
        var5 = IntVar()
        Checkbutton(edit, text="Labels       ", font="Helvetica 10", variable=var5).grid(row=17, sticky=W)

        # Handles third question and variables for each of the options
        Label(edit, text="What Type", font="Helvetica 16 bold", bg="#a3a3a3").grid(column=0, row=18, sticky=E)
        Label(edit, text="of Districts?", font="Helvetica 16 bold", bg="#a3a3a3").grid(column=1, row=18, sticky=W)
        var6 = IntVar()
        Checkbutton(edit, text="Armory", font="Helvetica 10", variable=var6).grid(row=19, sticky=W)
        var8 = IntVar()
        Checkbutton(edit, text="Castle", font="Helvetica 10", variable=var8).grid(row=20, sticky=W)
        var9 = IntVar()
        Checkbutton(edit, text="Cathedral", font="Helvetica 10", variable=var9).grid(row=21, sticky=W)
        var10 = IntVar()
        Checkbutton(edit, text="Courtyard", font="Helvetica 10", variable=var10).grid(row=22, sticky=W)
        var11 = IntVar()
        Checkbutton(edit, text="Farmland", font="Helvetica 10", variable=var11).grid(row=23, sticky=W)
        var12 = IntVar()
        Checkbutton(edit, text="Gate", font="Helvetica 10", variable=var12).grid(row=24, sticky=W)
        var13 = IntVar()
        Checkbutton(edit, text="Housing High", font="Helvetica 10", variable=var13).grid(row=25, sticky=W)
        var14 = IntVar()
        Checkbutton(edit, text="Housing Low", font="Helvetica 10", variable=var14).grid(row=26, sticky=W)
        var15 = IntVar()
        Checkbutton(edit, text="Housing Mid", font="Helvetica 10", variable=var15).grid(column=1, row=19, sticky=W)
        var16 = IntVar()
        Checkbutton(edit, text="Industrial", font="Helvetica 10", variable=var16).grid(column=1, row=20, sticky=W)
        var17 = IntVar()
        Checkbutton(edit, text="Market", font="Helvetica 10", variable=var17).grid(column=1, row=21, sticky=W)
        var18 = IntVar()
        Checkbutton(edit, text="Open Land", font="Helvetica 10", variable=var18).grid(column=1, row=22, sticky=W)
        var19 = IntVar()
        Checkbutton(edit, text="Park", font="Helvetica 10", variable=var19).grid(column=1, row=23, sticky=W)
        var20 = IntVar()
        Checkbutton(edit, text="Precinct", font="Helvetica 10", variable=var20).grid(column=1, row=24, sticky=W)
        var21 = IntVar()
        Checkbutton(edit, text="Shops", font="Helvetica 10", variable=var21).grid(column=1, row=25, sticky=W)
        var22 = IntVar()
        Checkbutton(edit, text="Slums", font="Helvetica 10", variable=var22).grid(column=1, row=26, sticky=W)

        def reset_info():
            """
            Resets the two global variables to allow basic map generation
            """
            global user_info
            user_info = [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
            global customize_info
            customize_info = [0, 1]

        # Creates the Go and Quit button
        Button(edit, text='Go', command=lambda: [var_states(), draw_map(canvas)]).grid(row=34, sticky=W, pady=4, padx=4)
        Button(edit, text='Reset', command=lambda: [reset_info(), draw_map(canvas)]).grid(row=34, sticky=E, pady=4,
                                                                                          padx=4)
        Button(edit, text='Quit', command=edit.destroy).grid(column=1, row=34, pady=4, padx=4)

    def save_file():
        """
        Saves the current map as a png.

        Support for .txt, which would allow the map to be reloaded and possibly edited is planned so long as we have
        edit options.
        """
        files = [('PNG', '*.png'),
                 ('All Files', '*.*'),
                 ('Text Document', '*.txt')]
        file = asksaveasfilename(filetypes=files, defaultextension=files)
        x = canvas.winfo_rootx()
        y = canvas.winfo_rooty()
        w = x + canvas.width
        h = y + canvas.height
        print(f"Grabbing screen from ({x}, {y}) to ({w}, {h})")
        ImageGrab.grab(bbox=(x, y, w, h)).save(file)
        # canvas.postscript(file="./postscript.ps")
        # Image.open("./postscript.ps").save(file)
        # os.remove("./postscript.ps")
        return

    # create the window object
    window = tk.Tk()
    window.title("Atlas")

    # creates the welcome window
    welcome = tk.Toplevel(window)
    welcome.title('Welcome Window')
    Label(welcome, text="Welcome to ATLAS", font="Helvetica 16 bold", bg="#a3a3a3", width=24).grid(row=0, sticky=W)
    Label(welcome, text="Hello user, thank you for downloading our map generator.\n "
                        "We hope that you enjoy our map generation and find the \n"
                        "edit, key and save functions useful.").grid(row=1, sticky=W)
    Label(welcome, text=" Directions:", font="Helvetica 16 bold", bg="#a3a3a3", width=24).grid(row=3, sticky=W)
    Label(welcome, text="To create a random map click generate.").grid(row=4, sticky=W)
    Label(welcome, text="To create your own map click edit.").grid(row=5, sticky=W)
    Label(welcome, text="If you need help click the help button.").grid(row=6, sticky=W)
    Button(welcome, text="Close", command=welcome.destroy).grid(row=7)

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
    button_frame.rowconfigure(12, weight=2)

    # Create the canvas that the picture will be rendered on
    canvas = ResizingCanvas(window, background="#ebd5b3")
    canvas.grid(column=1, row=0, sticky=('n', 's', 'e', 'w'))

    # Each of These are for the buttons that are created
    action_btn = tk.Button(button_frame, text="Generate", background="#4aa75d", foreground="black",
                           command=lambda: draw_map(canvas))  # Replace this with draw_map when I have it made
    action_btn.grid(column=0, row=0, sticky='w', padx=5, pady=5)

    save_btn = tk.Button(button_frame, text="Save", background="#a3a3a3", foreground="black",
                         command=lambda: save_file())
    save_btn.grid(column=0, row=1, sticky='w', padx=5, pady=5)

    edit_btn = tk.Button(button_frame, text="Edit", background="#a3a3a3", foreground="black", command=edit_msg)
    edit_btn.grid(column=0, row=2, sticky='w', padx=5, pady=5)

    key_btn = tk.Button(button_frame, text="Key", background="#a3a3a3", foreground="black", command=key_msg)
    key_btn.grid(column=0, row=3, sticky='w', padx=5, pady=5)

    help_btn = tk.Button(button_frame, text="Help", background="#a93939", foreground="black", command=help_msg)
    help_btn.grid(column=0, row=4, sticky='w', padx=5, pady=5)

    # Sets up and puts the image of the cardinal directions on the screen 
    img = tk.PhotoImage(file='../../images/compass.png')
    my_label = tk.Label(button_frame, image=img, background="#CCCCCC")
    my_label.grid(column=0, row=12, sticky='s', padx=10, pady=10)

    window.mainloop()


if __name__ == '__main__':
    main()
