from tkinter import Tk, ttk, Canvas, Frame, Button, Label, Entry, TOP, BOTTOM, LEFT, RIGHT, BOTH, HORIZONTAL
from PIL import ImageTk,  Image

class Window:
    def __init__(self, width: int, height: int, title: str = ""):
        self.root = Tk()
        self.root.title(title)
        # self.root.geometry(str(width) + "x" + str(height))

        self.width = width
        self.height = height
        self.primary_image = None

    def start(self):
        self.prepare_frame()
        self.root.mainloop()

    def prepare_frame(self):
        # image_select_frame = Frame(self.root, width = self.width, height = 50)
        view_frame = Frame(self.root)
        tag_frame = Frame(self.root, width = self.width, height = 50)
        entry_frame = Frame(self.root, width = self.width, height = 50)

        # image_select_frame.pack()
        view_frame.pack(fill = BOTH, expand = True)
        tag_frame.pack()
        entry_frame.pack()

        # Prepare View Frame
        self.primary_image = self.resize_image("images/stare.png", self.width)
        canvas = Canvas(view_frame, width = self.primary_image.width(), height = self.primary_image.height())
        canvas.pack(fill=BOTH, expand=True)
        desired_x = (1.5 *  self.primary_image.width()) // 2
        desired_y = self.primary_image.height() // 2
        canvas.create_image(desired_x, desired_y, image = self.primary_image)

        # Prepare Tag Frame
        tag_label = Label(tag_frame, text = "Tags: ", anchor = "w")
        tag_label.pack(side = LEFT)
        recent_tags = []
        for tag_number in range(1, 11):
            tag = Button(tag_frame, text = "Recent Tag " + str(tag_number))
            tag.pack(side = LEFT)
            recent_tags.append(tag)

        # Prepare Entry Frame
        tag_entry_label = Label(entry_frame, text = "Enter New Tag: ")
        tag_entry_label.pack(side = LEFT)
        tag_entry = Entry(entry_frame, width = 50)
        tag_entry.pack()

    def next_image(self):
        pass
    def previous_image(self):
        pass

    def get_scale_size_values(self, target_width: int, image_size: tuple) -> tuple:
        scale_factor = image_size[0] / target_width
        scaled_height = int(image_size[1] // scale_factor)

        return (target_width, scaled_height)

    def resize_image(self, relative_image_path: str, target_width: int) -> ImageTk.PhotoImage:
        image = Image.open(relative_image_path).convert("RGBA")
        
        return ImageTk.PhotoImage(image.resize(self.get_scale_size_values(target_width, image.size)))
    
    def display_image(self, relative_image_path: str) -> ImageTk.PhotoImage:
        image = Image.open(relative_image_path)
        return ImageTk.PhotoImage(image)
