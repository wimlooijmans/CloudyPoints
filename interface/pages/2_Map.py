import os
import streamlit as st
import numpy as np
import pandas as pd
import requests
from google.cloud import storage

from helper_functions import filter_image_names_on_city
import helper_variables


# Read cloud storage data
if os.path.exists("secrets/"):
    client = storage.Client.from_service_account_json(
        "secrets/cloudypoints-452719-847a44935e18.json"
    )
else:
    client = storage.Client()

bucket_name = "cp_bucket-1"
bucket = client.bucket(bucket_name=bucket_name, user_project=None)
blobs = client.list_blobs(bucket_name, prefix="data/test/", delimiter="/")

prefix = "data/test/"
all_filenames = [blob.name.removeprefix(prefix) for blob in blobs]

# Map Data
cities = ["Berlin", "Bielefeld", "Bonn", "Leverkusen", "Mainz", "Munich"]
cities_coordinates = np.array(
    [
        [52.52437, 13.41053],
        [52.03333, 8.53333],
        [50.73438, 7.09549],
        [51.033333, 6.983333],
        [49.992863, 8.247253],
        [48.13743, 11.57549],
    ]
)

map_column_names = ["latitude", "longitude"]
colors = ["#0cb2af", "#a1c65d", "#fac723", "#f29222", "#e95e50", "#936fac"]
sizes = [10, 50, 100, 500, 1000, 5000]

df_map_data = pd.DataFrame(cities_coordinates, columns=map_column_names)
df_map_data.insert(0, "City", cities)
df_map_data.insert(len(df_map_data.columns), "Color", colors)
df_map_data.insert(len(df_map_data.columns), "Size", sizes)


# Interface
st.map(df_map_data, color="Color", size="Size")

user_selection_city = st.selectbox(
    "Select a city:", cities, index=None, placeholder="Select city"
)

filtered_imgs = filter_image_names_on_city(user_selection_city, all_filenames)

user_selection_img_name = st.select_slider(
    "Select an image to preview",
    filtered_imgs,
)

suffix = "_left_image.png"
user_selection_blob = bucket.get_blob(prefix + user_selection_img_name + suffix)
user_selection_img_bytes = user_selection_blob.download_as_bytes()

# Request prediction
files_request = {"image": (user_selection_img_name + suffix, user_selection_img_bytes)}
response = requests.post(
    helper_variables.cp_serving_url,
    files=files_request,
    timeout=helper_variables.max_timeout,
)

images_container = st.container()

images_container.write("Image from test set - " + user_selection_img_name)
images_container.image(
    user_selection_img_bytes,
    caption=("Image from test set - " + user_selection_img_name),
)

images_container.write("")
images_container.write("Predicted Depth Image of " + user_selection_img_name)
images_container.image(
    response.content, caption="Predicted Depth Image of " + user_selection_img_name
)
