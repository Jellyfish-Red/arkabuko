import tkinter as tk
from tkinter import Tk, Canvas, Frame, Button, Label, Entry, simpledialog, LEFT, RIGHT, BOTH
from tkinter.ttk import Separator
from PIL import ImageTk, Image

from functools import partial

from model import Model

class View(Frame):
    def __init__(self, parent: Tk, model: Model, width: int, height: int):
        super().__init__(parent)
        self.parent = parent

        # Hard-Coded Constants TODO: Move to Config File
        self.MENU_BAR_HEIGHT = 30
        self.IMAGE_SELECT_WIDTH = 250
        self.IMAGE_SELECT_HEIGHT = 100
        self.VIEW_FRAME_HEIGHT = 450

        self.model = model

        # Window
        self.width = width
        self.height = height

        # Currently-selected image
        self.primary_image_canvas = None
        self.image_select_canvases = []
        self.image_select_image_list: list[(str, ImageTk.PhotoImage)] = []

    def start(self):
        self.prepare_window()

    def prepare_window(self):
        # Prepare Frames
        self.prepare_frames(self.width)
        self.prepare_menu_bar_frame(self.menu_bar_frame)
        self.display_view_label(self.search_description_frame, "all")
        self.prepare_image_select_frame(self.image_select_frame, self.IMAGE_SELECT_WIDTH, self.IMAGE_SELECT_HEIGHT)
        self.prepare_view_frame(self.view_frame, self.width, self.VIEW_FRAME_HEIGHT)
        self.prepare_tag_view_frame(self.tag_view_frame)
        self.prepare_tag_entry_frame(self.tag_entry_frame)

        # Prepare data shown in frames
        self.display_primary_image(self.primary_image_canvas, 
                                   self.model.get_selected_image_path())
        self.populate_image_select_frame(self.image_select_canvases)

    def prepare_frames(self, window_width):
        self.menu_bar_frame = Frame(self.parent, width = window_width)
        self.search_description_frame = Frame(self.parent, width = window_width, bg = "white")
        search_description_separator = Separator(self.parent, orient = "horizontal")
        self.image_select_frame = Frame(self.parent, width = window_width, height = self.IMAGE_SELECT_HEIGHT)
        image_select_separator = Separator(self.parent, orient = "horizontal")
        self.view_frame = Frame(self.parent, width = window_width)
        view_frame_separator = Separator(self.parent, orient = "horizontal")
        self.tag_view_frame = Frame(self.parent, width = window_width)
        self.tag_entry_frame = Frame(self.parent, width = window_width, height = 50)

        self.menu_bar_frame.pack(fill = BOTH, expand = True)
        self.search_description_frame.pack(fill = "x", expand = True)
        search_description_separator.pack(fill = "x", expand = True)
        self.image_select_frame.pack(fill = "x", expand = True)
        image_select_separator.pack(fill = "x", expand = True)
        self.view_frame.pack(fill = BOTH, expand = True)
        view_frame_separator.pack(fill = "x", expand = True)
        self.tag_view_frame.pack()
        self.tag_entry_frame.pack()

    def prepare_menu_bar_frame(self,
                               frame: tk.Frame):
        menu_bar = tk.Menu(frame)

        file_menu = tk.Menu(menu_bar, tearoff = 0)
        file_menu.add_command(label = "Save Tags", command = self.on_save_tags)
        file_menu.add_command(label = "Delete Tags from Selected Image", command = self.on_delete_tags)
        menu_bar.add_cascade(label = "File", menu = file_menu)

        search_menu = tk.Menu(menu_bar, tearoff = 0)
        search_menu.add_command(label = "Search Tag", command = self.on_search_tags)
        search_menu.add_command(label = "Reset Filter", command = self.on_reset_filter)
        menu_bar.add_cascade(label = "Search", menu = search_menu)

        self.parent.config(menu = menu_bar)

    def on_save_tags(self):
        self.model.save_tags()

    def on_delete_tags(self):
        self.model.delete_tags()
        self.regenerate_selected_image_tags(self.tag_view_frame)

    def on_search_tags(self):
        tag_to_search = simpledialog.askstring("Search Tags", "Enter a tag to search for")
        print(tag_to_search)

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

    def display_view_label(self, frame: tk.Frame, view_type: str):
        for widget in frame.winfo_children():
            if isinstance(widget, tk.Label) or isinstance(widget, tk.Button):
                widget.destroy()

        label_string = "Viewing "
        if view_type == "all":
            label_string += "all images in directory."
        else:
            label_string += "images tagged with \'" + view_type + "\'."
        label = tk.Label(frame, text = label_string, bg = "white")
        label.pack()

    def populate_image_select_frame(self, 
                                    canvases: list[tk.Canvas]):
        # Prepare variables
        self.image_select_image_list = []

        # Clear all images from canvases
        for canvas in canvases:
            canvas.delete("image_preview")

        # Generate list of valid image paths of images adjacent to the selected image
        adjacent_image_paths = self.model.get_adjacent_images()

        for i, image_path in enumerate(adjacent_image_paths):
            # If this image was considered valid, show it in the image select frame.
            # Otherwise, ignore it and move to the next loop.
            if image_path is not None:
                # Prepare image tag
                tag_bind_string = "image_preview"

                # Load and display the image on the canvas
                canvas = canvases[i]
                image = self.load_and_display_image(canvas, image_path, tag_bind_string)
                self.image_select_image_list.append((image_path, image))

    def load_and_display_image(self, canvas, image_path, image_tag) -> ImageTk.PhotoImage:
        # Load the image using Pillow
        pil_image = Image.open(image_path)
        target_width = canvas.winfo_reqwidth()
        tk_image = self.resize_image(pil_image, target_width)

        # Display the image on the canvas
        canvas.create_image(0, 0, anchor = tk.NW, image = tk_image, tags = image_tag)
        
        return tk_image

    def prepare_view_frame(self, frame: tk.Frame, width: int, height: int):
        # Use a default value for the width and height, just in case the image isn't selected yet
        if not self.primary_image_canvas:
            self.primary_image_canvas = Canvas(frame, width = width, height = height)
        self.primary_image_canvas.pack(fill=BOTH, expand=True)

    def prepare_tag_view_frame(self, frame: tk.Frame):
        # Prepare Tag View Frame
        tag_label = Label(frame, text = "Tags: ", anchor = "w")
        tag_label.pack(side = LEFT)
        
        self.regenerate_selected_image_tags(frame)

    def regenerate_selected_image_tags(self, frame: tk.Frame):
        for widget in frame.winfo_children():
            if isinstance(widget, tk.Button) or widget.cget("text") == "None":
                widget.destroy()
        
        if self.model.primary_image_tags is not None and len(self.model.primary_image_tags) > 0:
            for i in range(0, len(self.model.primary_image_tags)):
                tag = Button(frame, text = self.model.primary_image_tags[i])
                tag.config(command = partial(self.on_tag_click, tag.cget("text")))
                tag.pack(side = LEFT)
        else:
            tag_none_label = Label(frame, text = "None")
            tag_none_label.pack(side = LEFT)

    def on_tag_click(self, tag: str):
        tag_string = str(tag)
        self.display_view_label(self.search_description_frame, tag_string)
        self.model.regenerate_image_list(tag_string)
        self.populate_image_select_frame(self.image_select_canvases)
    
    def on_reset_filter(self):
        tag_string = "all"
        self.display_view_label(self.search_description_frame, tag_string)
        self.model.regenerate_image_list(None)
        self.populate_image_select_frame(self.image_select_canvases)


    def prepare_tag_entry_frame(self, frame: tk.Frame):
        # Prepare Entry Frame
        tag_entry_label = Label(frame, text = "Enter New Tag: ")
        tag_entry_label.pack(fill = "x", side = LEFT)

        self.tag_entry = Entry(frame, width = 50)
        self.tag_entry.pack(fill = "x", side = LEFT)

        self.tag_submit_button = Button(frame, text = "Submit")
        self.tag_submit_button.pack(fill = "x", side = LEFT)

    def display_primary_image(self, canvas: tk.Canvas, image_path: str, image_tag: str = "primary_image"):
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
