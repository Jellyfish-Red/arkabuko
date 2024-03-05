import tkinter as tk
from tkinter import Tk, ttk, Canvas, Frame, Button, Label, Entry, TOP, BOTTOM, LEFT, RIGHT, BOTH, HORIZONTAL
from PIL import ImageTk,  Image
from tagging import TagHandler

from os import listdir
from os.path import isfile, join, basename, abspath

class Window:
    def __init__(self, width: int, height: int, title: str, 
                 tag_handler: TagHandler = None, 
                 image_dir: str = None, 
                 last_image_path: str = None):
        
        if not image_dir:
            raise Exception("Requires image directory to be provided.")
        if not last_image_path:
            raise Exception("Requires currently-selected image to be provided")
        self.root = Tk()
        self.root.title(title)

        # Hard-Coded Constants TODO: Move to Config File
        self.IMAGE_SELECT_WIDTH = 250
        self.IMAGE_SELECT_HEIGHT = 100
        self.VIEW_FRAME_HEIGHT = 450

        # Window
        self.width = width
        self.height = height

        # Tags
        self.tag_handler = tag_handler

        # Selectable images
        self.image_directory = image_dir

        # Currently-selected image
        self.primary_image_filepath = join(image_dir, last_image_path)
        self.primary_image_canvas = None
        self.image_select_canvases = []

    def start(self):
        self.generate_image_list()
        self.prepare_window()
        self.root.mainloop()

    def prepare_window(self):
        self.prepare_frames(self.width)
        self.prepare_image_select_frame(self.image_select_frame, self.IMAGE_SELECT_WIDTH, self.IMAGE_SELECT_HEIGHT)
        self.prepare_view_frame(self.view_frame, self.width, self.VIEW_FRAME_HEIGHT)
        self.prepare_tag_view_frame()
        self.prepare_tag_suggestions_frame()
        self.prepare_tag_entry_frame()
        self.select_image(self.primary_image_canvas, join(self.image_directory, self.primary_image_filepath))
        self.populate_image_select_frame(self.image_select_canvases, self.primary_image_filepath, self.image_paths_list)

    def prepare_frames(self, window_width):
        self.image_select_frame = Frame(self.root, width = window_width, height = 50)
        self.view_frame = Frame(self.root, width = window_width)
        self.tag_view_frame = Frame(self.root, width = window_width, height = 50)
        self.tag_suggestions_frame = Frame(self.root, width = window_width, height = 50)
        self.tag_entry_frame = Frame(self.root, width = window_width, height = 50)

        self.image_select_frame.pack(fill = "x", expand = True)
        self.view_frame.pack(fill = BOTH, expand = True)
        self.tag_view_frame.pack()
        self.tag_suggestions_frame.pack()
        self.tag_entry_frame.pack()

    def prepare_image_select_frame(self,
                                   frame: tk.Frame,
                                   width: int,
                                   height: int):
        for widget in frame.winfo_children():
            if isinstance(widget, tk.Canvas):
                widget.destroy()
        self.image_select_canvases = []

        for i in range(0, 3):

            # Create a Canvas widget
            canvas = tk.Canvas(frame, width = width, height = height)
            canvas.pack(side = tk.LEFT, padx = 10)  # Adjust the placement as needed
            self.image_select_canvases.append(canvas)

            # Prepare tag for future images and link tag to event on click
            image_tag = "image_preview"
            
            if i == 0:
                canvas.tag_bind(image_tag, "<Button-1>", self.on_click_left_image)
            elif i == 1:
                canvas.tag_bind(image_tag, "<Button-1>", self.on_click_middle_image)
            elif i == 2:
                canvas.tag_bind(image_tag, "<Button-1>", self.on_click_right_image)

    def populate_image_select_frame(self, 
                                    canvases: list[tk.Canvas], 
                                    center_image_filepath: str, 
                                    image_paths: list[str]):
        # Prepare variables
        self.adjacent_image_list = []
        is_leftmost = False
        is_rightmost = False

        # Clear all images from canvases
        for canvas in canvases:
            canvas.delete("image_preview")

        # Get the images adjacent to the Primary.
        primary_image_index = image_paths.index(center_image_filepath)
        
        # Generate list of valid image paths
        image_select_paths = []
        for i in range(primary_image_index - 1, primary_image_index + 2):
            if 0 <= i < len(image_paths):
                image_select_paths.append(image_paths[i])
            elif i < 0:
                is_leftmost = True
                self.adjacent_image_list.append(("None", None))
            elif len(image_paths) <= i:
                is_rightmost = True

        for i, image_path in enumerate(image_select_paths):
            # If there are only two images to show because you're at the left-most image, 
            # leave the leftmost canvas blank and add 1 to the index
            if is_leftmost:
                i += 1

            # Prepare image tag
            image_tag = "image_preview"

            # Load and display the image on the canvas
            canvas = canvases[i]
            image = self.load_and_display_image(canvas, image_path, image_tag)
            self.adjacent_image_list.append((image_path, image))

    def on_click_left_image(self, event):
        image = self.adjacent_image_list[0]
        self.update_images(image)

    def on_click_middle_image(self, event):
        image = self.adjacent_image_list[1]
        self.update_images(image)

    def on_click_right_image(self, event):
        image = self.adjacent_image_list[2]
        self.update_images(image)

    def update_images(self, image):
        self.select_image(self.primary_image_canvas, image[0])
        self.populate_image_select_frame(self.image_select_canvases, image[0], self.image_paths_list)

    def load_and_display_image(self, canvas, image_path, image_tag) -> ImageTk.PhotoImage:
        # Load the image using Pillow
        pil_image = Image.open(image_path)
        target_width = canvas.winfo_reqwidth()
        tk_image = self.resize_image(pil_image, target_width)

        # Display the image on the canvas
        canvas.create_image(0, 0, anchor = tk.NW, image = tk_image, tags = image_tag)
        
        return tk_image

    def prepare_view_frame(self, frame: tk.Frame, width: int, height: int):
        # Prepare View Frame
        # Use a default value for the width and height, just in case the image isn't selected yet

        if not self.primary_image_canvas:
            self.primary_image_canvas = Canvas(self.view_frame, width = width, height = height)
        self.primary_image_canvas.pack(fill=BOTH, expand=True)

        # Create a Canvas widget
        canvas = tk.Canvas(frame, width=self.width, height=self.VIEW_FRAME_HEIGHT)
        canvas.pack(side=tk.LEFT, padx=10)  # Adjust the placement as needed

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

    def select_image(self, canvas: tk.Canvas, image_path: str, image_tag: str = "primary_image"):
        # Load and display the image on the canvas
        self.primary_image = self.load_and_display_image(canvas, image_path, image_tag)

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
    
    def delete_image_from_canvas(self, canvas: tk.Canvas, tag: str):
        canvas.delete(tag)

    # Generate a list of image file paths within the Image Directory
    def generate_image_list(self):
        self.image_paths_list = [join(self.image_directory, f) 
                                 for f in listdir(self.image_directory) 
                                 if isfile(join(self.image_directory, f))]
        print(self.image_paths_list)
