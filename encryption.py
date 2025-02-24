import cv2
import os

try:
    # Load cover image
    image_path = "photo.jpeg"
    
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Error: Cover image '{image_path}' not found!")
    
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Error: Failed to read the image. Ensure it's a valid image file.")

    # Input secret message and password
    msg = input("Enter secret message: ").strip()
    if not msg:
        raise ValueError("Error: Secret message cannot be empty!")

    password = input("Enter a passcode: ").strip()
    if not password:
        raise ValueError("Error: Passcode cannot be empty!")

    # Save the password to a file (for demonstration purposes only)
    try:
        with open("pass.txt", "w") as f:
            f.write(password)
    except Exception as e:
        raise IOError(f"Error writing to pass.txt: {e}")

    # Ensure the message fits in the image dimensions
    max_capacity = img.shape[0] * img.shape[1] * 3  # Total pixels * 3 color channels
    if len(msg) > max_capacity:
        raise ValueError("Error: Message is too long for this image!")

    # Embed the message into the image
    n, m, z = 0, 0, 0  # Row, column, and channel index
    for char in msg:
        try:
            img[n, m, z] = ord(char)  # Store ASCII value in a pixel channel
            n += 1
            m += 1
            z = (z + 1) % 3  # Cycle through the three channels
        except IndexError:
            raise ValueError("Error: Message embedding exceeded image size!")

    # Save the encrypted image
    output_filename = "encryptedPhoto.jpeg"
    if not cv2.imwrite(output_filename, img):
        raise IOError(f"Error: Failed to save encrypted image as '{output_filename}'!")

    # Open the encrypted image (platform-specific)
    try:
        if os.name == "nt":  # Windows
            os.system(f"start {output_filename}")
        elif os.name == "posix":  # macOS/Linux
            os.system(f"open {output_filename}" if "darwin" in os.sys.platform else f"xdg-open {output_filename}")
    except Exception as e:
        print(f"Error opening file: {e}")

    print("✅ Secret message successfully embedded into the image!")

except FileNotFoundError as e:
    print(e)
except ValueError as e:
    print(e)
except IOError as e:
    print(e)
except Exception as e:
    print(f"An unexpected error occurred: {e}")
