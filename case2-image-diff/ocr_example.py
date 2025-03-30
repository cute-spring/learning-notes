import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

# Path to your image file
img_path = "image/mobile_screen_1.jpeg"  # Replace with the actual path to your image

# Open the image using Pillow
image = Image.open(img_path)

# Convert to grayscale
gray_image = image.convert('L')

# Increase contrast
enhancer = ImageEnhance.Contrast(gray_image)
gray_image = enhancer.enhance(2)  # Increase contrast by a factor of 2

# Remove noise
gray_image = gray_image.filter(ImageFilter.MedianFilter())

# Apply thresholding (optional)
threshold_image = gray_image.point(lambda p: p > 200 and 255)

# Perform OCR on the processed image with configuration
extracted_text = pytesseract.image_to_string(threshold_image, lang='chi_sim', config='--psm 6')

print("Extracted Text:")
print(extracted_text)
