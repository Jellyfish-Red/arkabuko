import sys
from controller import Controller

def main() -> int:
    controller = Controller("", "", "", 800, 600, "Arkabuko - Image Viewer")
    controller.start()

if __name__ == '__main__':
    sys.exit(main())