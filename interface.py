from tkinter import Tk, ttk, Canvas, Frame, Button, Label, Entry, TOP, BOTTOM, LEFT, RIGHT, BOTH, HORIZONTAL
from PIL import ImageTk,  Image

class Window:
    def __init__(self, width: int, height: int, title: str = ""):
        self.root = Tk()
        self.root.title(title)
        # self.root.geometry(str(width) + "x" + str(height))

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
        self.primary_image = None

    def start(self):
        self.prepare_frame()
        self.root.mainloop()

    def prepare_frame(self):
        # image_select_frame = Frame(self.root, width = self.width, height = 50)
        view_frame = Frame(self.root, width = self.width, height = self.height - 50)
        tag_frame = Frame(self.root, width = self.width, height = 50)
        entry_frame = Frame(self.root, width = self.width, height = 50)

        # image_select_frame.pack()
        view_frame.pack()
        tag_frame.pack()
        entry_frame.pack()

        # Prepare View Frame
        canvas = Canvas(view_frame, bg="white", width = self.width, height = self.height - 50)
        canvas.pack(fill=BOTH, expand=True)
        self.primary_image = self.resize_image("images/d7eb66cf39dde20d54e53672ac8b3653.jpg", self.width)
        canvas.create_image(self.width // 2, self.height // 2, image = self.primary_image)

        # Prepare Tag Frame
        tag_label = Label(tag_frame, text = "Tags: ", anchor = "w")
        tag_label.pack(side = LEFT)
        recent_tags = []
        for tag_number in range(1, 11):
            tag = Button(tag_frame, text = "Recent Tag " + str(tag_number))
            tag.pack(side = LEFT)
            recent_tags.append(tag)

        # Prepare Entry Frame
        tag_entry_label = Label(entry_frame, text = "Enter New Tag: ")
        tag_entry_label.pack(side = LEFT)
        tag_entry = Entry(entry_frame, width = 50)
        tag_entry.pack()

    def next_image(self):
        pass
    def previous_image(self):
        pass

    def resize_image(self, relative_image_path: str, target_width: int) -> ImageTk.PhotoImage:
        image = Image.open(relative_image_path).convert("RGBA")
        
        scale_factor = image.width / target_width
        scaled_height = int(image.height // scale_factor)

        return ImageTk.PhotoImage(image.resize((target_width, scaled_height)))
    
    def display_image(self, relative_image_path: str) -> ImageTk.PhotoImage:
        image = Image.open(relative_image_path)
        return ImageTk.PhotoImage(image)
