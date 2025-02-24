import cv2
import os

try:
    # Check if OpenCV is installed
    if not hasattr(cv2, 'imread'):
        raise ImportError("Error: OpenCV (cv2) module not found! Install it using 'pip install opencv-python'.")

    # Load the encrypted image (lossless PNG format)
    image_path = "encryptedPhoto.png"
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Error: Encrypted image '{image_path}' not found!")

    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Error: Failed to read the encrypted image. Ensure it's a valid PNG image!")

    # Retrieve the stored password from file
    password_file = "pass.txt"
    if not os.path.exists(password_file):
        raise FileNotFoundError("Error: Password file not found!")

    try:
        with open(password_file, "r") as f:
            correct_pass = f.read().strip()
    except Exception as e:
        raise IOError(f"Error reading password file: {e}")

    # Ask user for the decryption passcode
    pas = input("Enter passcode for Decryption: ").strip()
    if pas != correct_pass:
        raise PermissionError("Error: Incorrect passcode. Access denied!")

    # Ask user for the secret message length
    try:
        length = int(input("Enter secret message length: ").strip())
        if length <= 0:
            raise ValueError("Error: Message length must be a positive integer.")
    except ValueError:
        raise ValueError("Error: Invalid length input! Please enter a valid number.")

    message = ""
    n, m, z = 0, 0, 0  # Row, column, and channel index

    # Read the embedded message from the image
    for i in range(length):
        if n >= img.shape[0] or m >= img.shape[1]:
            raise IndexError("Error: Reached image boundary before reading the full message.")

        message += chr(img[n, m, z])
        n += 1
        m += 1
        z = (z + 1) % 3  # Cycle through the channels

    print("✅ Decrypted message:", message)

except ImportError as e:
    print(e)
except FileNotFoundError as e:
    print(e)
except PermissionError as e:
    print(e)
except ValueError as e:
    print(e)
except IndexError as e:
    print(e)
except IOError as e:
    print(e)
except Exception as e:
    print(f"An unexpected error occurred: {e}")
