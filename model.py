from os import listdir
from os.path import abspath, exists, join, isfile

from config import Config
from tagging import TagHandler

class Model:
    def __init__(self):
        # Extract configuration information
        config_file_path = abspath("data/config.json")
        if not config_file_path:
            raise Exception("Configuration file not provided to Controller.")
        if not exists(config_file_path):
            raise Exception("Configuration file missing.")
        
        # Extract Image Folder Path and Tag File Path
        self.config = Config(config_file_path)
        
        if not self.config.get_image_dir():
            raise Exception("Requires image directory to be provided.")
        if not self.config.get_selected():
            raise Exception("Requires currently-selected image to be provided")

        # Set up Image Folder Path and Tag File variables
        if not self.config.get_image_dir():
            raise Exception("No Image directory location found in config file.")
        if not exists(self.config.get_image_dir()):
            raise Exception("Image folder missing")
        
        # Extract image tagging information that may already exist from previous use
        self.tag_handler = TagHandler(self.config.get_tag_filepath())

        # Set up image list and selected image
        self.regenerate_image_list()
        self.update_selected_image(join(self.config.get_image_dir(), self.config.get_selected()))

    def regenerate_image_list(self):
        image_directory = self.config.get_image_dir()
        self.image_paths_list = [join(image_directory, f) 
                                 for f in listdir(image_directory) 
                                 if isfile(join(image_directory, f))]
        print(self.image_paths_list)

    def get_selected_image_path(self):
        return self.image_paths_list[self.selected_image_index]
    
    def update_selected_image(self, path: str):
        try:
            self.selected_image_index = self.image_paths_list.index(path)
        except ValueError:
            self.selected_image_index = 0
        self.primary_image_tags = self.tag_handler.get(self.config.get_selected()) if not None else []

    def get_adjacent_images(self, radius = 1) -> list[str]:
        adjacent_image_paths = []
        for i in range(self.selected_image_index - radius, self.selected_image_index + radius + 1):
            if 0 <= i < len(self.image_paths_list):
                adjacent_image_paths.append(self.image_paths_list[i])
            else:
                adjacent_image_paths.append(None)

        return adjacent_image_paths
    
    def save_tags(self):
        self.model.tag_handler.pack()

    def add_tag(self, tag: str):
        self.primary_image_tags.append(tag)