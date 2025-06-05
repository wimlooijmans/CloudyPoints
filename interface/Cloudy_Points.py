import os
import streamlit as st

from helper_functions import check_model_api_status
import helper_variables

port_interface = os.getenv("PORT", "8501")
cp_interface_url = "http://0.0.0.0:" + port_interface
page_1_Depth_Estimation = "Depth_Estimation"
page_2_Select_image_from_test_set = "Select_image_from_test_set"

# Set page config
st.set_page_config(page_title="Cloudy Points", page_icon="☁️", layout="wide")

# Add API status check to sidebar
check_model_api_status(
    helper_variables.cp_serving_base_url, helper_variables.max_timeout
)

st.title("Cloudy Points ☁️")

st.write(
    "CloudyPoints is an application that provides Monocular Depth Estimation (MDE)."
)

st.write("")
st.write(
    "You can upload an image on the Depth Estimation page and a depth image will be returned:"
)
st.page_link("pages/1_Depth_Estimation.py", label="Depth Estimation", icon="⬆")

st.write("")
st.write(
    "If you do not have an image available to upload, you can select an image from the test set:"
)
st.page_link(
    "pages/2_Select_image_from_test_set.py",
    label="Select image from test set",
    icon=":material/photo_library:",
)

st.subheader("Example")
col_left, col_right = st.columns(2)

col_left.write("Cloudy Points will transform an image like this:")
col_left.image("images/berlin_000056_000019_left_image.png")

col_right.write("Into a depth image like this:")
col_right.image("images/prediction-berlin_000056_000019_left_image.png")
