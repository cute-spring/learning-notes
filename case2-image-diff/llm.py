import requests
import base64

# Function to encode image to base64
def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# API endpoint
url = "http://localhost:11434/api/chat"

# Image path
image_path = "image/mobile_screen_1.jpeg"  # Replace with your image path

# Encode image to base64
encoded_image = encode_image_to_base64(image_path)
# print(encoded_image)
# Define the payload
data = {
    "model": "llama3.2-vision:11b",
    "messages": [
        {
            "role": "user",
            "content": "what is in this image?",
            "images": [encoded_image]
        }
    ]
}

# Send the POST request
response = requests.post(url, json=data)

# Check the response
if response.status_code == 200:
    print("Response:", response.json())
else:
    print("Failed to get response. Status code:", response.status_code)