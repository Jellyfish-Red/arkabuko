from tkinter import Tk, ttk, Canvas, Frame, Button, Label, Entry, TOP, BOTTOM, LEFT, RIGHT, BOTH, HORIZONTAL
from PIL import ImageTk,  Image
from tagging import TagHandler

from os import listdir
from os.path import isfile, join

class Window:
    def __init__(self, width: int, height: int, title: str, tag_handler: TagHandler = None):
        self.root = Tk()
        self.root.title(title)
        # self.root.geometry(str(width) + "x" + str(height))

        # Window
        self.width = width
        self.height = height

        # Tags
        self.tag_handler = tag_handler
        self.primary_image_tag_list = []
        self.recent_tags = []

        # Selectable images
        self.image_directory = "/mnt/e/programming/development/arkabuko/images/"
        self.image_list = []

        # Currently-selected image
        self.primary_image = None
        self.primary_image_filepath = "images/stare.png"
        self.primary_image_canvas = None

        # Frames
        # image_select_frame = None
        self.view_frame = None
        self.tag_view_frame = None
        self.tag_suggestions_frame = None
        self.tag_entry_frame = None

    def start(self):
        self.generate_image_list()
        self.prepare_window()
        self.root.mainloop()

    def prepare_window(self):
        self.prepare_frames()
        self.prepare_view_frame()
        self.prepare_tag_view_frame()
        self.prepare_tag_suggestions_frame()
        self.prepare_tag_entry_frame()
        self.select_image(self.primary_image_filepath)


    def prepare_frames(self):
        # self.image_select_frame = Frame(self.root, width = self.width, height = 50)
        self.view_frame = Frame(self.root)
        self.tag_view_frame = Frame(self.root, width = self.width, height = 50)
        self.tag_suggestions_frame = Frame(self.root, width = self.width, height = 50)
        self.tag_entry_frame = Frame(self.root, width = self.width, height = 50)

        # self.image_select_frame.pack()
        self.view_frame.pack(fill = BOTH, expand = True)
        self.tag_view_frame.pack()
        self.tag_suggestions_frame.pack()
        self.tag_entry_frame.pack()

    def prepare_view_frame(self):
        # Prepare View Frame
        # Use a default value for the width and height, just in case the image isn't selected yet
        width = 800
        height = 450
        if self.primary_image is not None:
            width = self.primary_image.width()
            height = self.primary_image.height()

        self.primary_image_canvas = Canvas(self.view_frame, width = width, height = height)
        self.primary_image_canvas.pack(fill=BOTH, expand=True)

    def prepare_tag_view_frame(self):
        # Prepare Tag View Frame
        tag_label = Label(self.tag_view_frame, text = "Tags: ", anchor = "w")
        tag_label.pack(side = LEFT)
        # for tag_number in range(1, len(self.tag_handler.get(self.primary_image_filepath))):
        #     tag = Button(self.tag_view_frame, text = "Recent Tag " + str(tag_number))
        #     tag.pack(side = LEFT)
        #     recent_tags.append(tag)

    def prepare_tag_suggestions_frame(self):
        # Prepare Tag Suggestions Frame
        tag_suggestion_label = Label(self.tag_suggestions_frame, text = "Tag Suggestions: ", anchor = "w")
        tag_suggestion_label.pack(side = LEFT)
        # for tag_number in range(1, 11):
        #     tag = Button(self.tag_suggestions_frame, text = "Recent Tag " + str(tag_number))
        #     tag.pack(side = LEFT)
        #     self.recent_tags.append(tag)

    def prepare_tag_entry_frame(self):
        # Prepare Entry Frame
        tag_entry_label = Label(self.tag_entry_frame, text = "Enter New Tag: ")
        tag_entry_label.pack(side = LEFT)
        tag_entry = Entry(self.tag_entry_frame, width = 50)
        tag_entry.pack()

    def next_image(self):
        pass
    def previous_image(self):
        pass

    def select_image(self, target_image_file_path: str):
        # Determine if canvas clear is necessary
        if self.primary_image_filepath != target_image_file_path:
            if self.primary_image_canvas is not None:
                self.primary_image_canvas.delete("all")

        # Prepare primary image variables
        self.primary_image_filepath = target_image_file_path
        # self.primary_image_tag_list = self.tag_handler.get(self.primary_image_filepath)
        self.primary_image = self.resize_image(self.primary_image_filepath, self.width)
        
        # Display image on canvas
        desired_x = (1.5 *  self.primary_image.width()) // 2
        desired_y = self.primary_image.height() // 2
        self.primary_image_canvas.create_image(desired_x, desired_y, image = self.primary_image)

        self.prepare_view_frame()

    def get_scale_size_values(self, target_width: int, image_size: tuple) -> tuple:
        scale_factor = image_size[0] / target_width
        scaled_height = int(image_size[1] // scale_factor)

        return (target_width, scaled_height)

    def resize_image(self, image_path: str, target_width: int) -> ImageTk.PhotoImage:
        image = Image.open(image_path).convert("RGBA")
        
        return ImageTk.PhotoImage(image.resize(self.get_scale_size_values(target_width, image.size)))
    
    def display_image(self, image_path: str) -> ImageTk.PhotoImage:
        image = Image.open(image_path)
        return ImageTk.PhotoImage(image)

    def generate_image_list(self):
        self.image_list = [f for f in listdir(self.image_directory) if isfile(join(self.image_directory, f))]

