import json

class Config:
    def __init__(self, filepath: str):
        self.data = None
        self.__unpack(filepath)

    def __unpack(self, filepath: str):
        self.file_path = filepath
        with open(self.file_path) as f:
            self.data = json.load(f)

    def pack_file(self, filepath: str):
        self.file_path = filepath
        with open(self.file_path) as f:
            json.dump(self.tag_dictionary, f)
    
    def get_image_dir(self):
        return self.data['directory']
    
    def get_selected(self):
        return self.data['selected']