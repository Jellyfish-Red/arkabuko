from interface import Window
from tagging import TagHandler

class Controller:
    def __init__(self, default_image_folder_path: str, tag_file_path: str, config_file_path: str, width: int, height: int, title: str = ""):
        self.width = width
        self.height = height
        self.title = title
        self.image_folder_path = default_image_folder_path
        self.config_file_path = config_file_path
        self.tag_file_path = tag_file_path
        self.tag_handler = TagHandler()

    def start(self):
        # Start components
        # self.tag_handler.unpack_file(self.tag_file_path)
        self.__start_interface(self.width, self.height, self.title)

    def __start_interface(self, width: int, height: int, title: str = ""):
        self.window = Window(width, height, title)
        self.window.start()