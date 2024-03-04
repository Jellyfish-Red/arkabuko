import sys
from controller import Controller

def main() -> int:
    # primary_image = "stare.png" 
    primary_image = "ffxiv_01132024_194154_446.png"
    
    controller = Controller(800, 600, "Arkabuko - Image Viewer")
    controller.start()

if __name__ == '__main__':
    sys.exit(main())