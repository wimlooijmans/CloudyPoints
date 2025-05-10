import json
from ..interface.helper_functions import (
    extract_from_file_name,
    filter_file_names_on_city,
    filter_image_names_on_city,
)


def test_extract_from_file_name():
    assert extract_from_file_name("berlin_000000_000019_left_image.png") == (
        "berlin",
        "000000_000019",
    )
    assert extract_from_file_name("bielefeld_000000_032766_left_image.png") == (
        "bielefeld",
        "000000_032766",
    )
    assert extract_from_file_name("bonn_000010_000019_left_image.png") == (
        "bonn",
        "000010_000019",
    )
    assert extract_from_file_name("leverkusen_000037_000019_left_image.png") == (
        "leverkusen",
        "000037_000019",
    )
    assert extract_from_file_name("mainz_000000_004542_left_image.png") == (
        "mainz",
        "000000_004542",
    )
    assert extract_from_file_name("munich_000087_000019_left_image.png") == (
        "munich",
        "000087_000019",
    )


def test_filter_file_names_on_city():
    with open("tests/filenames_to_city_id.json", "r") as file:
        data = json.load(file)

    filenames = []

    for data_point in data:
        filenames.append(data_point["filename"])

    assert filter_file_names_on_city("berlin", filenames) == filenames[0:6]
    assert filter_file_names_on_city("bielefeld", filenames) == filenames[6:8]
    assert filter_file_names_on_city("leverkusen", filenames) == filenames[8:9]
    assert filter_file_names_on_city("mainz", filenames) == filenames[9:12]
    assert filter_file_names_on_city("munich", filenames) == filenames[12:]
    assert filter_file_names_on_city(None, filenames) == filenames


def test_filter_image_names_on_city():
    with open("tests/filenames_to_city_id.json", "r") as file:
        data = json.load(file)

    filenames = []
    image_names = []

    for data_point in data:
        filenames.append(data_point["filename"])
        image_names.append(data_point["city"] + "_" + data_point["img_id"])

    assert filter_image_names_on_city("berlin", filenames) == image_names[0:6]
    assert filter_image_names_on_city("bielefeld", filenames) == image_names[6:8]
    assert filter_image_names_on_city("leverkusen", filenames) == image_names[8:9]
    assert filter_image_names_on_city("mainz", filenames) == image_names[9:12]
    assert filter_image_names_on_city("munich", filenames) == image_names[12:]
    assert filter_image_names_on_city(None, filenames) == image_names
