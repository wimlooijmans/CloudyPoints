# Interface

The interface to showcase the application is build with Streamlit. It is deployed in a separate cloud run service. The home page displays a short description, links to the other pages and an example image. There are two other pages. The first page, *Depth Estimation*, gives the user the possibility to upload an image. Once uploaded, the image is displayed together with the depth map prediction. If the user does not have an image ready, he can go to the second page *Select image from test set*. This page lets the user select an image from the test set and shows the predicted depth map for that image.

## Code overview

The main page is defined in *Cloudy_Points.py*.

The page to upload an image is defined in *pages/1_Depth_Estimation.py*. If the user has uploaded an image, it is displayed. Next, a POST request is made to the model serving API to make a depth prediction from the image. The response depth image is displayed under the original image.

The page to select an image from the test set is defined in *pages/2_Select_image_from_test_set.py*. The page shows a drop-down menu to select a city where the test images are made. There is a slider under the drop-down menu that makes it possible for the user to select an image out of the test set from the chosen city. If no city is selected, the user can select from the whole test set. The image and depth map prediction are shown. Under the images is a map that shows in which cities the images in the test set were taken.

First, the code defines the necessary elements to connect to Google Cloud Storage and the storage buckets are defined. The test set images are stored in a Google Cloud Storage bucket and all the file names of these images are stored. Next, some data (cites, longitudes, latitudes,...) to construct the map is defined. Then, the interface is constructed. The filenames are filtered on the city selected by the user and passed as options to the slider element. The slider element returns a file name that is used to load the image from the cloud storage. Next, a POST request is made to the model serving API and the images are displayed.

Each page shows the status of the model serving API. This is defined in the *helper_variables.py*. A GET request is made to the model serving API and if a status code 200 is returned, text is displayed in the sidebar that the API is ready. This is done because it can take a few seconds to start up the model serving API.

*helper_functions.py* defines the function to write the model serving API status to the sidebar. It also defines some functions to create the list for the options in the selection slider, based on the chosen city.

*helper_variables.py* gets the model serving URL from the environment. If there is no ENV variable set, a default is set. This default is usually used when testing on a local machine. When deploying to a container or to the cloud, it is expected to provide the URL as an ENV variable.

*.streamlit/config.toml* stores settings for the Streamlit app. Here is defined that the user is only able to upload images with a maximum file size of 5 MB.

## Deployment

*.dockerignore* and *.gcloudignore* list the files and directories that should not be loaded when building an image for the application.

*requirements-interface.txt* lists the necessary packages for the interface application.

*Dockerfile* contains the info on how to build the image:
- Uses base image python:3.9-slim.
- Lists the files containing the code to be copied into the image.
- The port used is 8501.
- The required packages to be installed
- Run *Cloudy_Points.py*

The interface is deployed as a cloud run service. The deployment is automated in the CICD pipeline.
The command used is

```
gcloud run deploy ${{ inputs.interface-name }} \
--region=europe-west1 \
--source=$(pwd)/interface \
--platform managed \
--allow-unauthenticated \
--memory=512Mi \
--cpu=1 \
--update-env-vars=CP_BASE_URL="${{ env.MODEL_SERVING_BASE_URL }}" \
--build-service-account "SERVICE ACCOUNT" \
--quiet
```
Important to notice is that the base url for the model serving API should be set in the ENV variable CP_BASE_URL. Also, the build service account should be specified.
