from functools import partial
from tkinter import Entry
from PIL import ImageTk

from os import listdir
from os.path import join, isfile

from model import Model
from view import View

class Controller:
    def __init__(self, model: Model, view: View):
        self.model = model
        self.view = view
        
        # Hook up Image Select Callbacks
        image_tag = "image_preview"
        
        for i, canvas in enumerate(self.view.image_select_canvases):
            if i == 0:
                canvas.tag_bind(image_tag, "<Button-1>", self.on_click_left_image)
            elif i == 1:
                canvas.tag_bind(image_tag, "<Button-1>", self.on_click_middle_image)
            elif i == 2:
                canvas.tag_bind(image_tag, "<Button-1>", self.on_click_right_image)

        # Hook up Tag Callbacks
        on_tag_image_command = partial(self.on_tag_image, self.view.tag_entry)
        self.view.tag_submit_button.configure(command = on_tag_image_command)

    def on_click_left_image(self, event):
        image_path = self.view.image_select_image_list[0]
        self.select_image(image_path)

    def on_click_middle_image(self, event):
        image_path = self.view.image_select_image_list[1]
        self.select_image(image_path)

    def on_click_right_image(self, event):
        image_path = self.view.image_select_image_list[2]
        self.select_image(image_path)

    def select_image(self, image: tuple[str, ImageTk.PhotoImage]):
        path = image[0]
        print(path)
        if path is not None or path != "":
            self.model.update_selected_image(path)
            self.view.display_primary_image(self.view.primary_image_canvas, path)
            self.view.populate_image_select_frame(self.view.image_select_canvases, path, self.model.get_adjacent_images())

    def on_tag_image(self, tag_entry: Entry):
        tag_text = tag_entry.get()
        print(tag_text)
        self.model.add_tag(tag_text)