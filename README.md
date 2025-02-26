# Secure Data Hiding in Images using Steganography (Python)

This project showcases a straightforward implementation of image steganography using Python and OpenCV. It enables users to securely embed (encrypt) a secret message within an image and later extract (decrypt) it via a user-friendly GUI built with Tkinter.

---

## 🚀 Features

### 🔒 Data Hiding (Encryption)
- Embed a secret text message into a cover image.
- The message's ASCII values are written into the image pixels using a diagonal embedding technique.
- Saves the modified image as a **lossless PNG** to maintain data integrity.

### 🔑 Decryption
- Extract the hidden message from the modified image.
- Requires the correct **passcode** and **message length** to retrieve data.

### 🖥️ Graphical User Interface (GUI)
A Tkinter-based interface simplifies the entire process:
- 📂 **Upload** a cover image.
- ✍️ **Enter** a secret message and passcode.
- 🔏 **Encrypt** (hide) the message in the image.
- 📂 **Upload** an encrypted image.
- 🔓 **Decrypt** (extract) the hidden message.

---

## 📌 Requirements

Make sure you have the following installed:

- **Python 3.x**
- **OpenCV** – Install using pip:
  ```bash
  pip install opencv-python
  ```
- **Tkinter** (Pre-installed with Python on most systems)

---

## 🎯 Usage Instructions

1. **Run the script** to launch the application.
2. **Select an image** and enter the message to hide.
3. **Encrypt** the message into the image and save it.
4. **Upload the encrypted image** for decryption.
5. **Enter the passcode** to reveal the hidden message.

---

## 📸 Preview

(Include screenshots showcasing the UI for encryption and decryption)

---

This project provides a fundamental yet effective approach to steganography, ensuring secure data hiding within images. 🚀
