import cv2
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Create the main application window
root = tk.Tk()
root.title("Image Steganography - Encryption")
root.geometry("500x500")
root.configure(bg="#f0f0f0")

# Global variable to store the selected cover image path
cover_image_path = None

# Styling
style = ttk.Style()
style.configure("TButton", font=("Arial", 10), padding=5)
style.configure("TLabel", font=("Arial", 10))
style.configure("TEntry", padding=5)


def load_cover_image():
    """Function to load the cover image for encryption."""
    global cover_image_path
    file_path = filedialog.askopenfilename(filetypes=[("JPEG files", "*.JPEG")])
    if file_path:
        cover_image_path = file_path
        cover_label.config(text=f"Selected: {os.path.basename(file_path)}", foreground="black")


def encrypt_message():
    """Function to embed a secret message into the image."""
    global cover_image_path

    try:
        if not cover_image_path:
            raise FileNotFoundError("Please select a cover image first.")

        # Read the image
        img = cv2.imread(cover_image_path)
        if img is None:
            raise ValueError("Invalid image format! Please select a valid PNG image.")

        # Get user input for message and passcode
        secret_message = enc_message_entry.get().strip()
        passcode = enc_password_entry.get().strip()

        if not secret_message:
            raise ValueError("Secret message cannot be empty!")
        if not passcode:
            raise ValueError("Passcode cannot be empty!")

        # Save the passcode in a text file
        with open("pass.txt", "w") as f:
            f.write(passcode)

        # Embed the message into the image
        n, m, z = 0, 0, 0  # Row, column, and channel index
        for char in secret_message:
            if n >= img.shape[0] or m >= img.shape[1]:
                raise IndexError("Message too long! Reduce the length or use a bigger image.")

            img[n, m, z] = ord(char)
            n += 1
            m += 1
            z = (z + 1) % 3  # Cycle through the RGB channels

        # Ask user where to save the encrypted image
        save_path = filedialog.asksaveasfilename(defaultextension=".JPEG", filetypes=[("JPEG files", "*.JPEG")])
        if save_path:
            cv2.imwrite(save_path, img)
            messagebox.showinfo("Success", f"Message encrypted and saved as:\n{save_path}")

    except FileNotFoundError as e:
        messagebox.showerror("File Error", str(e))
    except ValueError as e:
        messagebox.showerror("Input Error", str(e))
    except IndexError as e:
        messagebox.showerror("Encryption Error", str(e))
    except Exception as e:
        messagebox.showerror("Unexpected Error", f"An error occurred: {e}")


# --- Cover Image Section (For Encryption) ---
cover_frame = ttk.LabelFrame(root, text="Cover Image (For Encryption)")
cover_frame.pack(fill="x", padx=10, pady=5)
btn_load_cover = ttk.Button(cover_frame, text="Load Cover Image", command=load_cover_image)
btn_load_cover.pack(pady=5)
cover_label = ttk.Label(cover_frame, text="No file selected", foreground="gray")
cover_label.pack(pady=5)

# --- Encryption Section ---
enc_frame = ttk.LabelFrame(root, text="Encryption")
enc_frame.pack(fill="x", padx=10, pady=5)
ttk.Label(enc_frame, text="Secret Message:").pack()
enc_message_entry = ttk.Entry(enc_frame, width=50)
enc_message_entry.pack(pady=5)
ttk.Label(enc_frame, text="Passcode:").pack()
enc_password_entry = ttk.Entry(enc_frame, width=50, show="*")
enc_password_entry.pack(pady=5)
btn_encrypt = ttk.Button(enc_frame, text="Encrypt", command=encrypt_message)
btn_encrypt.pack(pady=5)

# Run the Tkinter event loop
root.mainloop()
