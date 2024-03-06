import sys
from tkinter import Tk

from model import Model
from view import View
from controller import Controller

class Application(Tk):
    def __init__(self):
        # Initialize Parent UI frame
        super().__init__()
        self.title("Arkabuko - Image Viewer")

        # Prepare MVC components
        model = Model()
        view = View(self, model, 800, 600)
        view.start()
        
        controller = Controller(model, view)

def main() -> int:
    app = Application()
    app.mainloop()

if __name__ == '__main__':
    sys.exit(main())