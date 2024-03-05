import sys
from controller import Controller
from os.path import basename, abspath, join

def main() -> int:
    config_rel_file_path = "data/config.json"
    
    controller = Controller(800, 600, "Arkabuko - Image Viewer", 
                            config_file_path = abspath(config_rel_file_path))
    controller.start()

if __name__ == '__main__':
    sys.exit(main())