import tkinter as tk
from tkinter import Tk, ttk, Canvas, Frame, Button, Label, Entry, TOP, BOTTOM, LEFT, RIGHT, BOTH, HORIZONTAL
from PIL import ImageTk,  Image
from tagging import TagHandler

from os import listdir
from os.path import isfile, join, basename, abspath

class Window:
    def __init__(self, width: int, height: int, title: str, tag_handler: TagHandler = None):
        self.root = Tk()
        self.root.title(title)
        # self.root.geometry(str(width) + "x" + str(height))

        # Hard-Coded Constants TODO: Move to Config File
        self.IMAGE_SELECT_WIDTH = 250
        self.IMAGE_SELECT_HEIGHT = 100
        self.VIEW_FRAME_HEIGHT = 450

        # Window
        self.width = width
        self.height = height

        # Tags
        self.tag_handler = tag_handler
        self.primary_image_tag_list = []
        self.recent_tags = []

        # Selectable images
        self.image_directory = "/mnt/e/programming/development/arkabuko/images/"
        self.image_paths_list = []

        # Currently-selected image
        self.primary_image = []
        # self.primary_image_filepath = "stare.png" 
        self.primary_image_filepath = "ffxiv_01132024_194154_446.png"
        self.primary_image_canvas = None

        # Adjacent images
        self.adjacent_image_list = []

        # Frames
        self.image_select_frame = None
        self.view_frame = None
        self.tag_view_frame = None
        self.tag_suggestions_frame = None
        self.tag_entry_frame = None

        # Selectable images
        self.selectable_images = None

    def start(self):
        self.generate_image_list()
        self.prepare_window()
        self.root.mainloop()

    def prepare_window(self):
        self.prepare_frames(self.width)
        self.prepare_view_frame()
        self.prepare_tag_view_frame()
        self.prepare_tag_suggestions_frame()
        self.prepare_tag_entry_frame()
        self.select_image(self.primary_image_canvas, self.image_directory + self.primary_image_filepath)
        self.populate_image_select_frame(self.image_select_frame, self.primary_image_filepath, self.image_paths_list)

    def prepare_frames(self, window_width):
        self.image_select_frame = Frame(self.root, width = window_width, height = 50, bg = "red")
        self.view_frame = Frame(self.root, width = window_width)
        self.tag_view_frame = Frame(self.root, width = window_width, height = 50)
        self.tag_suggestions_frame = Frame(self.root, width = window_width, height = 50)
        self.tag_entry_frame = Frame(self.root, width = window_width, height = 50)

        self.image_select_frame.pack(fill = "x", expand = True)
        self.view_frame.pack(fill = BOTH, expand = True)
        self.tag_view_frame.pack()
        self.tag_suggestions_frame.pack()
        self.tag_entry_frame.pack()

    def populate_image_select_frame(self, 
                                    frame: tk.Frame, 
                                    center_image_filepath: str, 
                                    image_paths: list[str]):
        # Prepare variables
        self.adjacent_image_list = []
        for widget in frame.winfo_children():
            if isinstance(widget, tk.Canvas):
                widget.destroy()

        # Get the images adjacent to the Primary.
        primary_image_index = image_paths.index(center_image_filepath)
        
        # Generate list of valid image paths
        image_select_paths = []
        for i in range(primary_image_index - 1, primary_image_index + 2):
            if 0 <= i < len(image_paths):
                image_select_paths.append(image_paths[i])

        print(image_select_paths)
        
        for i, image_path in enumerate(image_select_paths):
            # Prepare image tag
            image_tag = "image_preview_" + str(i)

            # Create a Canvas widget
            canvas = tk.Canvas(frame, width=self.IMAGE_SELECT_WIDTH, height=self.IMAGE_SELECT_HEIGHT)
            canvas.pack(side=tk.LEFT, padx=10)  # Adjust the placement as needed

            # Load and display the image on the canvas
            self.load_and_display_image(canvas, image_path, self.adjacent_image_list, image_tag)

    def load_and_display_image(self, canvas, image_path, image_list, image_tag):
        # Load the image using Pillow
        pil_image = Image.open(image_path)
        target_width = canvas.winfo_reqwidth()
        tk_image = self.resize_image(pil_image, target_width)

        # Display the image on the canvas
        canvas.create_image(0, 0, anchor = tk.NW, image = tk_image, tags = image_tag)

        # Store the PhotoImage in the list to prevent garbage collection
        image_list.append(tk_image)

    def prepare_view_frame(self):
        # Prepare View Frame
        # Use a default value for the width and height, just in case the image isn't selected yet
        width = self.width
        height = self.VIEW_FRAME_HEIGHT
        # if self.primary_image is not None:
        #     width = self.primary_image.width()
        #     height = self.primary_image.height()

        if not self.primary_image_canvas:
            self.primary_image_canvas = Canvas(self.view_frame, width = width, height = height)
        self.primary_image_canvas.pack(fill=BOTH, expand=True)

    def prepare_tag_view_frame(self):
        # Prepare Tag View Frame
        tag_label = Label(self.tag_view_frame, text = "Tags: ", anchor = "w")
        tag_label.pack(side = LEFT)
        
        # list_tags = self.tag_handler.get(self.primary_image_filepath)
        # if list_tags is None:
        #     no_tags_label = Label(self.tag_view_frame, text = "None", anchor = "e")
        #     no_tags_label.pack(side = RIGHT)

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

    def select_image(self, canvas: tk.Canvas, target_image_file_path: str):
        # Determine if canvas clear is necessary
        if self.primary_image_filepath != target_image_file_path:
            if canvas is not None:
                canvas.delete("all")

        # Prepare primary image variables
        self.primary_image = []
        self.primary_image_filepath = target_image_file_path
        self.load_and_display_image(canvas, self.primary_image_filepath, self.primary_image, "primary_image")

    def get_scale_size_values(self, target_width: int, image_size: tuple) -> tuple:
        scale_factor = image_size[0] / target_width
        scaled_height = int(image_size[1] // scale_factor)

        return (target_width, scaled_height)
    
    def resize_image(self, image: ImageTk.PhotoImage, target_width: int) -> ImageTk.PhotoImage:
        image = image.convert("RGBA")
        return ImageTk.PhotoImage(image.resize(self.get_scale_size_values(target_width, image.size)))
    
    def display_image(self, image_path: str) -> ImageTk.PhotoImage:
        image = Image.open(image_path)
        return ImageTk.PhotoImage(image)

    # Generate a list of image file paths within the Image Directory
    def generate_image_list(self):
        self.image_paths_list = [join(self.image_directory, f) for f in listdir(self.image_directory) if isfile(join(self.image_directory, f))]
