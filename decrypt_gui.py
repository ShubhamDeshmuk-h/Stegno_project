import cv2
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext

# Create the main application window
root = tk.Tk()
root.title("Image Steganography")
root.geometry("500x500")
root.configure(bg="#f0f0f0")

# Global variable to store the selected encrypted image path
encrypted_image_path = None

# Styling
style = ttk.Style()
style.configure("TButton", font=("Arial", 10), padding=5)
style.configure("TLabel", font=("Arial", 10))
style.configure("TEntry", padding=5)


def load_encrypted_image():
    """Function to load the encrypted image."""
    global encrypted_image_path
    file_path = filedialog.askopenfilename(filetypes=[("JPEG files", "*.JPEG")])
    if file_path:
        encrypted_image_path = file_path
        encrypted_label.config(text=f"Selected: {os.path.basename(file_path)}", foreground="black")


def decrypt_message():
    """Function to decrypt the message from the encrypted image with error handling."""
    global encrypted_image_path

    try:
        if not encrypted_image_path:
            raise FileNotFoundError("Please select an encrypted image first.")

        # Load the encrypted image
        img = cv2.imread(encrypted_image_path)
        if img is None:
            raise ValueError("Failed to read the encrypted image. Ensure it's a valid PNG image!")

        # Retrieve the stored password
        password_file = "pass.txt"
        if not os.path.exists(password_file):
            raise FileNotFoundError("Password file not found!")

        with open(password_file, "r") as f:
            correct_pass = f.read().strip()

        # Get passcode input from the GUI
        pas = dec_password_entry.get().strip()
        if pas != correct_pass:
            raise PermissionError("Incorrect passcode. Access denied!")

        # Get secret message length from the GUI
        try:
            length = int(dec_length_entry.get().strip())
            if length <= 0:
                raise ValueError("Message length must be a positive integer.")
        except ValueError:
            raise ValueError("Invalid message length! Please enter a valid number.")

        message = ""
        n, m, z = 0, 0, 0  # Row, column, and channel index

        # Read the embedded message from the image
        for i in range(length):
            if n >= img.shape[0] or m >= img.shape[1]:
                raise IndexError("Reached image boundary before reading the full message.")

            message += chr(img[n, m, z])
            n += 1
            m += 1
            z = (z + 1) % 3  # Cycle through the channels

        # Display the decrypted message in the text box
        dec_text.delete(1.0, tk.END)
        dec_text.insert(tk.END, message)
        messagebox.showinfo("Success", "Message decrypted successfully!")

    except FileNotFoundError as e:
        messagebox.showerror("File Error", str(e))
    except PermissionError as e:
        messagebox.showerror("Access Denied", str(e))
    except ValueError as e:
        messagebox.showerror("Input Error", str(e))
    except IndexError as e:
        messagebox.showerror("Decryption Error", str(e))
    except Exception as e:
        messagebox.showerror("Unexpected Error", f"An unexpected error occurred: {e}")


# --- Encrypted Image Section (For Decryption) ---
encrypted_frame = ttk.LabelFrame(root, text="Encrypted Image (For Decryption)")
encrypted_frame.pack(fill="x", padx=10, pady=5)
btn_load_encrypted = ttk.Button(encrypted_frame, text="Load Encrypted Image", command=load_encrypted_image)
btn_load_encrypted.pack(pady=5)
encrypted_label = ttk.Label(encrypted_frame, text="No file selected", foreground="gray")
encrypted_label.pack(pady=5)

# --- Decryption Section ---
dec_frame = ttk.LabelFrame(root, text="Decryption")
dec_frame.pack(fill="x", padx=10, pady=5)
ttk.Label(dec_frame, text="Passcode:").pack()
dec_password_entry = ttk.Entry(dec_frame, width=50, show="*")
dec_password_entry.pack(pady=5)
ttk.Label(dec_frame, text="Message Length:").pack()
dec_length_entry = ttk.Entry(dec_frame, width=50)
dec_length_entry.pack(pady=5)
btn_decrypt = ttk.Button(dec_frame, text="Decrypt", command=decrypt_message)
btn_decrypt.pack(pady=5)
ttk.Label(dec_frame, text="Decrypted Message:").pack()
dec_text = scrolledtext.ScrolledText(dec_frame, width=50, height=5)
dec_text.pack(pady=5)

# Run the Tkinter event loop
root.mainloop()
