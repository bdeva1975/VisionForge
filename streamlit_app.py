import streamlit as st
from app import generate_image_variation, edit_image, preprocess_image
from PIL import Image
import requests
import io
from io import BytesIO

st.title("Image Variation and Editing Generator")

option = st.radio("Choose an option:", ("Generate Variation", "Edit Image"))

if option == "Generate Variation":
    uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

        if st.button("Generate Variation"):
            with st.spinner("Generating variation..."):
                variation_urls = generate_image_variation(uploaded_file)
                
                if variation_urls:
                    for i, url in enumerate(variation_urls):
                        response = requests.get(url)
                        img = Image.open(BytesIO(response.content))
                        st.image(img, caption=f"Variation {i+1}", use_column_width=True)
                else:
                    st.error("Failed to generate image variation. Please try again.")

elif option == "Edit Image":
    uploaded_file = st.file_uploader("Choose an image to edit...", type=["png", "jpg", "jpeg"])
    mask_file = st.file_uploader("Choose a mask image (optional, transparent PNG)...", type=["png"])
    prompt = st.text_input("Enter a prompt describing what to add or remove:")

    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

        if mask_file:
            st.image(mask_file, caption="Mask Image", use_column_width=True)

        if st.button("Edit Image"):
            if not prompt:
                st.error("Please enter a prompt before editing the image.")
            else:
                with st.spinner("Editing image..."):
                    # If no mask is provided, create a transparent mask
                    if not mask_file:
                        img = Image.open(uploaded_file)
                        mask = Image.new("RGBA", img.size, (0, 0, 0, 0))
                        mask_byte_arr = io.BytesIO()
                        mask.save(mask_byte_arr, format="PNG")
                        mask_byte_arr.seek(0)
                        mask_file = mask_byte_arr

                    edited_urls = edit_image(uploaded_file, mask_file, prompt)
                    
                    if edited_urls:
                        for i, url in enumerate(edited_urls):
                            response = requests.get(url)
                            img = Image.open(BytesIO(response.content))
                            st.image(img, caption=f"Edited Image {i+1}", use_column_width=True)
                    else:
                        st.error("Failed to edit image. Please try again.")