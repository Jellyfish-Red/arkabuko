from interface import Window
from tagging import TagHandler

class Controller:
    def __init__(self, width: int, height: int, title: str = "", 
                 image_folder_path: str = None, 
                 tag_file_path: str = None, 
                 config_file_path: str = None):
        # # Extract configuration information
        # if not config_file_path:
        #     raise Exception("Configuration file missing.")
        
        # # TODO: Add Config file processing. Extract Image Folder Path and Tag File Path
        
        # # Set up Image Folder Path and Tag File variables
        # if not image_folder_path:
        #     raise Exception("Image folder missing")
        
        # self.tag_handler = TagHandler()

        # if tag_file_path:
        #     self.tag_handler.unpack_file(tag_file_path)

        # Handle remaining program information.
        self.width = width
        self.height = height
        self.title = title
        self.image_folder_path = image_folder_path
        self.config_file_path = config_file_path
        self.tag_file_path = tag_file_path

    def start(self):
        # Start components
        # self.tag_handler.unpack_file(self.tag_file_path)
        self.__start_interface(self.width, self.height, self.title)

    def __start_interface(self, width: int, height: int, title: str = ""):
        self.window = Window(width, height, title)
        self.window.start()