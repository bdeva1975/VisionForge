import os
from dotenv import load_dotenv
from openai import OpenAI
from PIL import Image
import io

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def preprocess_image(image_file, max_size_mb=4):
    # Open the image
    img = Image.open(image_file)
    
    # Convert to RGBA mode
    img = img.convert('RGBA')
    
    # Convert to PNG
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    
    # Check size
    size_mb = len(img_byte_arr) / (1024 * 1024)
    if size_mb > max_size_mb:
        # Reduce size if it's too large
        while size_mb > max_size_mb:
            width, height = img.size
            img = img.resize((int(width*0.9), int(height*0.9)), Image.LANCZOS)
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            size_mb = len(img_byte_arr) / (1024 * 1024)
    
    return img_byte_arr

def generate_image_variation(image_file, n=1, size="1024x1024"):
    try:
        processed_image = preprocess_image(image_file)
        response = client.images.create_variation(
            image=processed_image,
            n=n,
            size=size
        )
        return [data.url for data in response.data]
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def edit_image(image_file, mask_file, prompt, n=1, size="1024x1024"):
    try:
        processed_image = preprocess_image(image_file)
        processed_mask = preprocess_image(mask_file) if mask_file else None
        response = client.images.edit(
            image=processed_image,
            mask=processed_mask,
            prompt=prompt,
            n=n,
            size=size
        )
        return [data.url for data in response.data]
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
