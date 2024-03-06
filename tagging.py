import json
from os.path import abspath, exists

class TagHandler:
    def __init__(self, filepath: str = None):
        # If no file path was given, assume there is no file and create a new one at the default location.
        if not filepath:
            default_path = "data/tags.json"
            with open(default_path, 'w') as file:
                json.dump({}, file)

            self.file_path = abspath(default_path)

        # If a file path was given but no file exists, create a file at that file path.
        elif not exists(filepath):
            self.file_path = abspath(filepath)
            with open(self.file_path, 'w') as file:
                json.dump({}, file)

        # Otherwise, or if you have passed through either of the aforementioned checks, make sure to safe the file path.
        else:
            self.file_path = abspath(filepath)

        # You are now ready to unpack the file.
        self.__unpack()

    def __unpack(self):
        with open(self.file_path) as f:
            self.tag_dictionary = json.load(f)

    def pack(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.tag_dictionary, f)
            print(self.tag_dictionary)

    def add(self, image_file_path: str, tag: str):
        # Create tag list for image if necessary.
        if image_file_path not in self.tag_dictionary:
            self.tag_dictionary[image_file_path] = []
        
        # Add tag to tag list if not already there.
        if tag not in self.tag_dictionary[image_file_path]:
            self.tag_dictionary[image_file_path].append(tag)

        # Do nothing if tag already exists in tag list.
            
    def remove(self, image_file_path: str, tag: str):
        if len(self.tag_dictionary) == 0:
            return
        
        # Remove tag only if file exists in dictionary and if tag exists in tag list.
        if image_file_path in self.tag_dictionary:
            if tag in self.tag_dictionary[image_file_path]:
                self.tag_dictionary[image_file_path].remove(tag)

    def get(self, image_file_path: str) -> list[str]:
        if len(self.tag_dictionary) == 0:
            return None
        
        if image_file_path not in self.tag_dictionary:
            return None
        
        return self.tag_dictionary[image_file_path]
        
    def contains(self, image_file_path: str, tag: str) -> bool:
        # Create tag list for image if necessary.
        if image_file_path not in self.tag_dictionary:
            return False
        
        return tag in self.tag_dictionary[image_file_path]