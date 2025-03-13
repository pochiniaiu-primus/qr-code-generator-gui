import tkinter as tk


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

        self.canvas.create_window(200, 50, window=self.label)

        self.name_label = tk.Label(self.root, text="Link name", font=("Arial", 15))
        self.link_label = tk.Label(self.root, text="Link", font=("Arial", 15))
        self.canvas.create_window(200, 100, window=self.name_label)
        self.canvas.create_window(200, 160, window=self.link_label)

        self.name_entry = tk.Entry(self.root, width=60)
        self.canvas.create_window(200, 120, window=self.name_entry)

        self.link_entry = tk.Entry(self.root, width=60)
        self.canvas.create_window(200, 180, window=self.link_entry)

        self.generate_qr_button = tk.Button(
            self.root, text="Generate QR code", width=51,
            command="", highlightthickness=0
        )
        self.canvas.create_window(200, 220, window=self.generate_qr_button)
