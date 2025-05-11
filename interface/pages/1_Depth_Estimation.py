import streamlit as st
import requests

from helper_functions import check_model_api_status
import helper_variables


# Set page config
st.set_page_config(layout="wide")

# Add API status check to sidebar
check_model_api_status(
    helper_variables.cp_serving_base_url, helper_variables.max_timeout
)

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
