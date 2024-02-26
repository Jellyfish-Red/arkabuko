from tkinter import Tk, ttk, Canvas, Frame, Button, Label, TOP, BOTTOM, LEFT, RIGHT, BOTH, HORIZONTAL
from PIL import ImageTk,  Image

class Window:
    def __init__(self, width: int, height: int, title: str = ""):
        self.root = Tk()
        self.root.title(title)
        self.root.geometry(str(width) + "x" + str(height))

        self.width = width
        self.height = height

        self.__running = False
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.root.update_idletasks()
        self.root.update()

    def wait_for_close(self):
        self.__running = True

        while self.__running:
            self.redraw()

    def close(self):
        self.__running = False


class Viewer(Window):
    def __init__(self, width: int, height: int, title: str = ""):
        super().__init__(width, height, title)

    def start(self):
        self.prepare_test_frame()
        self.root.mainloop()

    def prepare_test_frame(self):
        view_frame = Frame(self.root, width = self.width, height = self.height - 50)
        tag_frame = Frame(self.root, width = self.width, height = 50)
        # entry_frame = Frame(self.root, width = self.width, height = 50)

        view_frame.pack(side = TOP)
        tag_frame.pack()
        # entry_frame.pack(side=BOTTOM)

        canvas = Canvas(view_frame, bg="white", width = self.width, height = self.height - 50)
        canvas.pack(fill=BOTH, expand=True)
        test_image = self.resize_image("images/d7eb66cf39dde20d54e53672ac8b3653.jpg", self.width)
        canvas.create_image(self.width // 2, self.height // 2, image = test_image)

        test_label = Label(tag_frame, text = "Tags: ", anchor = "w")
        test_label.pack(side = LEFT)
        recent_tags = []
        for tag_number in range(1, 11): # TODO: Convert to grid?
            tag = Button(tag_frame, text = "Recent Tag " + str(tag_number))
            tag.pack()
            recent_tags.append(tag)
        
        # self.root.after(50, self.prepare_test_frame)
        self.root.mainloop()


    def resize_image(self, relative_image_path: str, target_width: int) -> ImageTk.PhotoImage:
        image = Image.open(relative_image_path).convert("RGBA")
        
        scale_factor = image.width / target_width
        scaled_height = int(image.height // scale_factor)

        return ImageTk.PhotoImage(image.resize((target_width, scaled_height)))
    
    def display_image(self, relative_image_path: str) -> ImageTk.PhotoImage:
        image = Image.open(relative_image_path)
        return ImageTk.PhotoImage(image)
