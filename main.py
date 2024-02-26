import sys
from interface import Window

def main() -> int:
    window = Window(800, 600, "Arkabuko - Image Viewer")
    window.wait_for_close()


if __name__ == '__main__':
    sys.exit(main())