from interface import Window
from config import Config
from tagging import TagHandler

class Controller:
    def __init__(self, width: int, height: int, title: str = "", 
                 tag_file_path: str = None, 
                 config_file_path: str = None):
        # # Extract configuration information
        # if not config_file_path:
        #     raise Exception("Configuration file missing.")
        
        # Extract Image Folder Path and Tag File Path
        self.config = Config(config_file_path)

        # # Set up Image Folder Path and Tag File variables
        # if not image_folder_path:
        #     raise Exception("Image folder missing")
        
        # self.tag_handler = TagHandler()
        # self.tag_handler.unpack(tag_file_path)

        # if tag_file_path:
        #     self.tag_handler.unpack_file(tag_file_path)

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
                             image_dir = self.config.get_image_dir(), 
                             last_image_path = self.config.get_selected())
        self.window.start()