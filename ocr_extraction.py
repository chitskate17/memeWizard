from PIL import Image
import pytesseract

# Image path
image_path = "convo1.png"

# Open image with Pillow
img = Image.open(image_path)

# Process image and extract text
text = pytesseract.image_to_string(img)

print(text)
