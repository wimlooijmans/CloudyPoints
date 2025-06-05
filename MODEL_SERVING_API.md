# API Implementation

An API is implemented to serve the model. The app is made in Flask and the code can be found in the *src/* folder.

## Code Overview

### Model

The class MiDaSFineTuner is defined in the *src/model_loader.py* file. The model was previously trained on a local machine and the weights are stored on Google Cloud Storage. The weights get loaded from this location in *src/run.py* by an url.

### Flask App
A Flask app is created to serve the model and provide an API to run inference. This is defined in *src/run.py*.

Paths are defined as on a local file system, since the bucket to read from and write to is mounted during deployment. The model gets loaded from the *src/model_loader.py* file and the weights are downloaded by an url from Google Cloud Storage. The Flask app provides two routes.

The first route is the base url, which provides a basic welcome page and returns a response code 200.

The second route is the */predict* route. This can be used to send an image over a POST request. First, some checks are done (file name, image size). Then, the image is stored on Google Cloud Storage. Next, the image is resized, loaded into a tensor and the model is called to run inference. The result from the model is scaled and transformed in a colored image that represents to show the depth in the image. This output image is resized, stored in Google Cloud Storage and returned as response on the request.

## Deployment

The Model Serving API is deployed in a Google Cloud Run service. It gets automatically deployed by the CICD pipeline. The code to deploy is:

```
gcloud run deploy ${{ inputs.model-serving-api-name }} \
--region=europe-west1 \
--source=$(pwd) \
--allow-unauthenticated \
--memory=8Gi \
--cpu=2 \
--add-volume name=cp_volume_user_data,type=cloud-storage,bucket=cp_bucket_user_data \
--add-volume-mount volume=cp_volume_user_data,mount-path=/mnt/user_data_storage \
--build-service-account "SERVICE ACCOUNT" \
--quiet
```

Note that this applications requires 8 Gi of memory. Because of this, minimal 2 CPUs have to be used. Two arguments `--add-volume name` and `--add-volume-mount` are used to mount the Google Cloud Storage bucket as a local file system in the deployed app. The build service account should be specified.

Files and folders to ignore are listed in the *.dockerignore* and *.gcloudignore* files in the root directory.

The necessary packages are listed in *requirements.txt* in the root directory.

The *Dockerfile* in the root directory describes how to build the image. The base image used is *python:3.12-slim*. To run the server, gunicorn is used with 1 worker and 8 threads. Important is to use the `--preload` argument and the `--timeout 120` argument, so the application has enough time to download the model and weights.
