import os
import streamlit as st
import requests

port_interface = os.getenv("PORT", "8501")
cp_interface_url = "http://localhost:" + port_interface
page_1_Depth_Estimation = "Depth_Estimation"

cp_serving_base_url = os.getenv("CP_BASE_URL", "http://127.0.0.1:5001")

st.set_page_config(page_title="Cloudy Points", page_icon="☁️", layout="wide")

st.title("Cloudy Points ☁️")

st.markdown(
    f"""
    CloudyPoints is an application that provides Monocular Depth Estimation (MDE).

    You can upload an image on the
    <a href="{cp_interface_url}/{page_1_Depth_Estimation}" target="_self">Depth Estimation page</a>
     and a depth image will be returned.
    """,
    unsafe_allow_html=True,
)

st.subheader("Example")
col_left, col_right = st.columns(2)

col_left.write("Cloudy Points will transform an image like this:")
col_left.image("images/berlin_000056_000019_left_image.png")

col_right.write("Into a depth image like this:")
col_right.image("images/prediction-berlin_000056_000019_left_image.png")

with st.sidebar:
    st.write("**Status**")
    status = "Model Serving API Starting. Please wait..."
    placeholder = st.empty()

    placeholder.write(status)
    response = requests.get(cp_serving_base_url)
    if response.status_code == 200:
        status = "Model Serving API Ready"
        placeholder.write(status)
