# Interface
This folder contains the source code files for the Streamlit interface application

## Docker Container
To run the code in a docker container, open terminal and cd into the interface directory.
Then, run the commands below in terminal.

**Build image:**
```
docker build --platform linux/amd64 --file interface.Dockerfile -t cp-interface:latest .
```
Change to:
```
docker build --platform linux/amd64 -t cp-interface:latest .
```

**Run container:**
```
docker run -p 8501:8501 -e CP_BASE_URL="http://192.168.0.213:5001" cp-interface:latest
```
Change the ENV variable CP_BASE_URL to the correct url of the model serving API.

## Deploy to Google Cloud
Make sure to cd to the interface directory and run:
```
gcloud run deploy cp-interface \
--region=europe-west1 \
--source=$(pwd) \
--platform managed \
--allow-unauthenticated \
--memory=512Mi \
--cpu=1 \
--update-env-vars=CP_BASE_URL="https://cp-model-serving-api-436098836644.europe-west1.run.app"
--build-service-account projects/cloudypoints-452719/serviceAccounts/github-actions-sa@cloudypoints-452719.iam.gserviceaccount.com \
--quiet
```

--ignore-file=interface.Dockerfile.dockerignore \
