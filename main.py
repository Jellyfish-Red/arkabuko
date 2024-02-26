import sys
from interface import Window
from viewer import Viewer

def main() -> int:
    window = Window(800, 600, "Arkabuko - Image Viewer")
    viewer = Viewer(window)
    window.wait_for_close()


if __name__ == '__main__':
    sys.exit(main())