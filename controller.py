from functools import partial
from tkinter import Entry, END
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
        tag_bind_string = "image_preview"
        
        for i, canvas in enumerate(self.view.image_select_canvases):
            if i == 0:
                canvas.tag_bind(tag_bind_string, "<Button-1>", self.on_click_left_image)
            elif i == 1:
                canvas.tag_bind(tag_bind_string, "<Button-1>", self.on_click_middle_image)
            elif i == 2:
                canvas.tag_bind(tag_bind_string, "<Button-1>", self.on_click_right_image)

        self.view.parent.bind("<Left>", self.on_click_left_image)
        self.view.parent.bind("<Right>", self.on_click_right_image)

        # Hook up Tag Functionality Callbacks
        on_tag_image_command = partial(self.on_tag_image, self.view.tag_entry)
        self.view.tag_submit_button.configure(command = on_tag_image_command)

        on_entry_return_command = partial(self.on_return_press, self.view.tag_entry)
        self.view.tag_entry.bind("<Return>", on_entry_return_command)

    def on_click_left_image(self, event):
        self.select_image(-1)

    def on_click_middle_image(self, event):
        self.select_image(0)

    def on_click_right_image(self, event):
        self.select_image(1)

    def select_image(self, offset: int):
        if 0 <= self.model.selected_image_index + offset < len(self.model.image_paths_list):
            image_path = self.model.image_paths_list[self.model.selected_image_index + offset]
            print(image_path)

            if image_path is not None or image_path != "":
                self.model.update_selected_image(image_path)
                self.view.display_primary_image(self.view.primary_image_canvas, image_path)
                self.view.populate_image_select_frame(self.view.image_select_canvases)
                self.view.regenerate_selected_image_tags(self.view.tag_view_frame)

    def on_tag_image(self, tag_entry: Entry):
        tag_text = tag_entry.get()
        if not self.model.tag_handler.contains(self.model.get_selected_image_path(), tag_text):
            self.model.add_tag(tag_text)
            self.view.regenerate_selected_image_tags(self.view.tag_view_frame)
            tag_entry.delete(0, END)
            print(f"Added tag: {tag_text}")

    def on_return_press(self, tag_entry: Entry, event):
        self.on_tag_image(tag_entry)