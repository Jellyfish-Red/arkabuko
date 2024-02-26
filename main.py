import sys
from interface import Window

def main() -> int:
    window = Window(800, 600, "Arkabuko - Image Viewer")
    # viewer.wait_for_close()
    window.start()


if __name__ == '__main__':
    sys.exit(main())