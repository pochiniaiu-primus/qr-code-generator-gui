import tkinter as tk

import pyqrcode
from PIL import ImageTk, Image


class GUI:

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("QR Code Generator")
        self.root.geometry("500x700")
        self.root.config(padx=10, pady=10)

        self.canvas = tk.Canvas(self.root, width=400, height=600)
        self.canvas.pack()

        self.label = tk.Label(self.root, text="QR Code Generator", fg='blue',
                              font=("Arial", 30))

        self.canvas.create_window(200, 30, window=self.label)

        self.name_label = tk.Label(self.root, text="Link name", font=("Arial", 15))
        self.link_label = tk.Label(self.root, text="Link", font=("Arial", 15))
        self.canvas.create_window(200, 70, window=self.name_label)
        self.canvas.create_window(200, 130, window=self.link_label)

        self.name_entry = tk.Entry(self.root, width=60)
        self.canvas.create_window(200, 100, window=self.name_entry)

        self.link_entry = tk.Entry(self.root, width=60)
        self.canvas.create_window(200, 160, window=self.link_entry)

        self.generate_qr_button = tk.Button(
            self.root, text="Generate QR code", width=30,
            command=lambda: self.generate_gr(self.name_entry.get(), self.link_entry.get()),
            highlightthickness=0
        )
        self.canvas.create_window(200, 190, window=self.generate_qr_button)

        self.clear_name_button = tk.Button(
            self.root, text="Clear name", width=30,
            command=lambda: self.clear_name(),
            highlightthickness=0
        )
        self.canvas.create_window(200, 220, window=self.clear_name_button)

        self.clear_link_button = tk.Button(
            self.root, text="Clear link", width=30,
            command=lambda: self.clear_link(),
            highlightthickness=0
        )
        self.canvas.create_window(200, 250, window=self.clear_link_button)

        self.exit_button = tk.Button(
            self.root, text="Exit", width=30,
            command=self.root.quit, highlightthickness=0
        )
        self.canvas.create_window(200, 280, window=self.exit_button)

    def clear_name(self):
        self.name_entry.delete(0, 'end')

    def clear_link(self):
        self.link_entry.delete(0, 'end')

    def generate_gr(self, link_name, link):
        file_name = link_name + ".png"
        url = pyqrcode.create(link)
        url.png(file_name, scale=8)

        image = ImageTk.PhotoImage(Image.open(file_name))

        image_label = tk.Label(image=image)

        image_label.image = image

        self.canvas.create_window(200, 450, window=image_label)
