import copy
from os import listdir
from os.path import abspath, exists, join, isfile, dirname

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
        self.primary_image_tags = []

        # Set up currently-selected image variables
        self.selected_path = join(self.config.get_image_dir(), self.config.get_selected())

        # Set up image list and selected image
        image_directory = self.config.get_image_dir()
        self.full_image_paths_list: list[str] = [join(image_directory, file_name) 
                                                 for file_name in listdir(image_directory) 
                                                 if isfile(join(image_directory, file_name))]
        self.regenerate_image_list(None)
        self.update_selected_image(self.selected_path)

    def regenerate_image_list(self, tag: str):
        self.image_paths_list = []
        if tag is not None:
            subset = self.tag_handler.get_subset(tag)
            for full_file_path in self.full_image_paths_list:
                if full_file_path in subset:
                    path = subset[subset.index(full_file_path)]
                    self.image_paths_list.append(full_file_path)

            # Assume selected image is guaranteed to be in filtered list TODO fix
            self.update_selected_image(self.selected_path)
        else:
            self.image_paths_list = copy.deepcopy(self.full_image_paths_list)
            self.update_selected_image(self.selected_path)
            
        # print(self.image_paths_list)

    def get_selected_image_path(self):
        return self.image_paths_list[self.selected_image_index]
    
    def update_selected_image(self, path: str):
        try:
            self.selected_image_index = self.image_paths_list.index(path)
            self.selected_path = self.image_paths_list[self.selected_image_index]
        except ValueError:
            self.selected_image_index = 0
            self.selected_path = ""

        tags = self.tag_handler.get(self.get_selected_image_path())
        self.primary_image_tags = tags if tags != None else []

    def get_adjacent_images(self, radius: int = 1) -> list[str]:
        adjacent_image_paths = []
        for i in range(self.selected_image_index - radius, self.selected_image_index + radius + 1):
            if 0 <= i < len(self.image_paths_list):
                adjacent_image_paths.append(self.image_paths_list[i])
            else:
                adjacent_image_paths.append(None)

        return adjacent_image_paths
    
    def save_tags(self):
        self.tag_handler.pack()

    def delete_tag(self, tag: str):
        self.tag_handler.remove(self.selected_path, tag)

    def delete_tags(self):
        self.tag_handler.remove_all(self.selected_path)
        self.tag_handler.pack()

    def add_tag(self, tag: str):
        self.tag_handler.add(self.get_selected_image_path(), tag)
        self.primary_image_tags.append(tag)