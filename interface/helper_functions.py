import streamlit as st
import requests


def check_model_api_status(url, max_time_out):
    with st.sidebar:
        st.write("**Status**")
        status = "Model Serving API Starting. Please wait..."
        placeholder = st.empty()

        placeholder.write(status)
        response = requests.get(url, timeout=max_time_out)
        if response.status_code == 200:
            status = "Model Serving API Ready"
            placeholder.write(status)


def extract_from_file_name(file_name):
    """
    Extracts the city and the image id from the filename

    Args:
        file_name (str): The file name

    Returns:
        city (str)
        image_id (str)
    """

    split = file_name.split("_")
    city = split[0]
    image_id = split[1] + "_" + split[2]

    return city, image_id


def filter_file_names_on_city(city_to_filter, file_names):
    """
    Returns a list with all the file names from the given city.
    If the given city is None, a list with all file names is returned.

    Args:
        city_to_filter (str): The city to filter on
        file_names (list): List with all the file names

    Returns:
        filtered_file_names (list): List with all the file names for the given city, or all file names if city is None.
    """

    if city_to_filter is None:
        filtered_file_names = file_names
    else:
        indexes = [
            i
            for i, filename in enumerate(file_names)
            if extract_from_file_name(filename)[0] == city_to_filter.lower()
        ]
        filtered_file_names = [file_names[idx] for idx in indexes]

    return filtered_file_names


def filter_image_names_on_city(city_to_filter, file_names):
    """
    Returns a list with all the image names (city_imgid) from the given city.
    If the given city is None, a list with all image names is returned.

    Args:
        city_to_filter (str): The city to filter on
        file_names (list): List with all the file names

    Returns:
        filtered_names (list): List with all the image names for the given city, or all image names if city is None.
    """

    filtered_file_names = filter_file_names_on_city(city_to_filter, file_names)

    filtered_names = []
    for file_name in filtered_file_names:
        city, image_id = extract_from_file_name(file_name)
        filtered_names.append(city + "_" + image_id)

    return filtered_names
