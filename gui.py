import io
import tkinter as tk
from tkinter import messagebox, filedialog
import pyqrcode
from PIL import ImageTk, Image
import logging

logging.basicConfig(
    filename="qr_generator.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class GUI:

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("QR Code Generator")
        self.root.geometry("500x700")
        self.root.config(padx=10, pady=10)
        self.qr_data = None

        # Create a canvas to place widgets.
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
            command=lambda: self.generate_gr(self.link_entry.get()),
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

        self.download_button = tk.Button(
            self.root, text="Download QR Code", width=30,
            command=lambda: self.save_qr(), highlightthickness=0
        )
        self.canvas.create_window(200, 615, window=self.download_button)

    def clear_name(self):
        self.name_entry.delete(0, 'end')

    def clear_link(self):
        self.link_entry.delete(0, 'end')

    def generate_gr(self, link: str):
        """
        Generate a QR code image from the provided link and display it on the canvas.
        :param link: The URL to encode in the QR code.
        """
        if not link:
            logging.warning("No link provided.")
            messagebox.showwarning("Warning", "No link provided.")
            return
        try:
            # Create a QR code object from the provided link using pyqrcode.
            qr = pyqrcode.create(link)
        except Exception as e:
            logging.error(f"Error creating QR code: {e}")
            messagebox.showerror("Error", f"Error creating QR code: {e}")
            return
        # Use an in-memory byte buffer.
        buffer = io.BytesIO()
        try:
            qr.png(buffer, scale=4, module_color=[255, 255, 255, 255], background=[22, 56, 83, 255])
        except Exception as e:
            logging.error(f"Error generating PNG in buffer: {e}")
            messagebox.showerror("Error", f"Error generating PNG in buffer: {e}")
            return

        # Store the generated PNG data for later saving.
        self.qr_data = buffer.getvalue()

        buffer.seek(0)  # Reset the buffer pointer to the beginning.
        try:
            # Open the image from the buffer and convert it to a Tkinter-compatible image.
            image = ImageTk.PhotoImage(Image.open(buffer))
        except Exception as e:
            logging.error(f"Error converting buffer to PhotoImage: {e}")
            messagebox.showerror("Error", f"Error converting buffer to PhotoImage: {e}")
            return
        # Create a label widget to hold and display the QR code image.
        image_label = tk.Label(self.canvas, image=image)
        # Retain a reference to the image to prevent it from being garbage collected.
        image_label.image = image
        # Display the image label on the canvas.
        self.canvas.create_window(200, 450, window=image_label)

    def save_qr(self):
        """
        Save the generated QR code image to disk.
        """
        if not hasattr(self, 'qr_data') or self.qr_data is None:
            logging.warning("Please generate a QR code before saving.")
            messagebox.showwarning("Warning", "Please generate a QR code before saving.")
            return

        default_name = self.name_entry.get().strip() or "QRCode"
        file_path = filedialog.asksaveasfilename(
            initialfile=default_name,
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
            title="Save QR Code"
        )

        if file_path:
            try:
                # Write the QR code PNG data to the chosen file.
                with open(file_path, "wb") as file:
                    file.write(self.qr_data)
                logging.info(f"QR Code saved to {file_path}")
                messagebox.showinfo("Success", f"QR Code successfully saved to {file_path}")
            except Exception as e:
                logging.error(f"Error saving QR code: {e}")
                messagebox.showerror("Error", f"Error saving QR code: {e}")
