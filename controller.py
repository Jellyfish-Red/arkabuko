from interface import Window
from config import Config
from tagging import TagHandler

from os.path import exists

class Controller:
    def __init__(self, width: int, height: int, title: str = "", 
                 config_file_path: str = None):
        # Extract configuration information
        if not config_file_path:
            raise Exception("Configuration file not provided to Controller.")
        if not exists(config_file_path):
            raise Exception("Configuration file missing.")
        
        # Extract Image Folder Path and Tag File Path
        self.config = Config(config_file_path)

        # Set up Image Folder Path and Tag File variables
        if not self.config.get_image_dir():
            raise Exception("No Image directory location found in config file.")
        if not exists(self.config.get_image_dir()):
            raise Exception("Image folder missing")
        
        self.tag_handler = TagHandler(self.config.get_tag_filepath())

        # Handle remaining program information.
        self.width = width
        self.height = height
        self.title = title

    def start(self):
        # Start components
        # self.tag_handler.unpack_file(self.tag_file_path)
        self.__start_interface(self.width, self.height, self.title)

    def __start_interface(self, width: int, height: int, title: str = ""):
        self.window = Window(width, height, title, 
                             tag_handler = self.tag_handler,
                             image_dir = self.config.get_image_dir(), 
                             last_image_path = self.config.get_selected())
        self.window.start()