import streamlit as st
from pathlib import Path
import os
import google.generativeai as genai

GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]="AIzaSyAtl0EsC3qIZxw-5VHFZWH9aNrrIcbta-s"
genai.configure(api_key=GOOGLE_API_KEY)


# Set up the model
generation_config = {
  "temperature": 0.4,
  "top_p": 1,
  "top_k": 32,
  "max_output_tokens": 6000,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_ONLY_HIGH"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_ONLY_HIGH"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_ONLY_HIGH"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_ONLY_HIGH"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro-vision-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

# Validate that an image is present
if not (img := Path("image.jpg")).exists():
  raise FileNotFoundError(f"Could not find image: {img}")

image_parts = [
  {
    "mime_type": "image/jpeg",
    "data": Path("image.jpg").read_bytes()
  },
]

# Streamlit Interface
st.header("Gemini Pro Vision Image Analysis")

uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Store image temporarily 
    img_path = "temp_image.jpg" 
    with open(img_path, 'wb') as f:
        f.write(uploaded_file.getvalue())

    # Image and Prompt Preparation
    image_parts = [
        {
            "mime_type": uploaded_file.type,
            "data": Path(img_path).read_bytes()
        }
    ]

    prompt_parts = [
    image_parts[0],
    "your role is of a helpeful and very knowledgeable assistant to a doctor LLM model. Now what you have to do is thoroughly analyze the given image and generate a detailed explaination on what is the condition shown in the image, now your valuable insights from the image will be key for the doctor LLM model to understand what's the condition of the patient from the image and generate a detailed explaination you can use medical lingo and be as comprehensive as possible and suggest treatments "
    ]

    # Send Request & Display Output
    with st.spinner("Analyzing Image..."):
        response = model.generate_content(prompt_parts)
        st.subheader("Analysis Result:")
        st.write(response.text) 

    # Remove temporary image (optional)
    if os.path.exists(img_path):
        os.remove(img_path)




