from tkinter import Tk, BOTH, Canvas

class Window:
    def __init__(self, width, height, title = ""):
        self.__root = Tk()
        self.__root.title(title)
        self.__canvas = Canvas(self.__root, bg="white", width=width, height=height)
        self.__canvas.pack(fill=BOTH, expand=1)

        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def draw_line(self, line, color):
        line.draw(self.__canvas, color)
    
    def draw_cell(self, cell):
        cell.draw()

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True

        while self.__running:
            self.redraw()

    def close(self):
        self.__running = False