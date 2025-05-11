import streamlit as st
import requests
from pathlib import Path
from io import BytesIO, BufferedReader

import helper_variables

path_src = Path(__file__).resolve().parent
path_user_data_storage = path_src.parent / "mnt" / "user_data_storage"
path_uploads = path_user_data_storage / "uploads"
path_predictions = path_user_data_storage / "predictions"

with st.sidebar:
    st.write("**Status**")
    status = "Model Serving API Starting. Please wait..."
    placeholder = st.empty()

    placeholder.write(status)
    response = requests.get(helper_variables.cp_serving_base_url)
    if response.status_code == 200:
        status = "Model Serving API Ready"
        placeholder.write(status)

st.title("Depth Estimation")
st.markdown(
    """
    This page allows you to upload an image (max 5 MB).
    A depth estimation will be returned.
    """
)

uploaded_image = st.file_uploader(
    "Upload Image:",
    ["jpg", "jpeg", "png"],
)

images_container = st.container()

if uploaded_image is not None:
    file_name = uploaded_image.name
    file_type = uploaded_image.type

    # Show image
    images_container.subheader("Image")
    images_container.image(
        uploaded_image,
        caption=file_name,
    )

    # Transform to
    uploaded_image_bytes = uploaded_image.getvalue()
    uploaded_image_file_like = BytesIO(uploaded_image_bytes)
    uploaded_image_buffered_reader = BufferedReader(uploaded_image_file_like)

    # Request prediction
    files_request = {"image": uploaded_image}
    response = requests.post(
        helper_variables.cp_serving_url,
        files=files_request,
        timeout=helper_variables.max_timeout,
    )

    images_container.subheader("Predicted Depth Image")
    images_container.image(
        response.content, caption="Predicted Depth Image of " + file_name
    )
