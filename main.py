import sys
from interface import Viewer

def main() -> int:
    viewer = Viewer(800, 600, "Arkabuko - Image Viewer")
    # viewer.wait_for_close()
    viewer.start()


if __name__ == '__main__':
    sys.exit(main())