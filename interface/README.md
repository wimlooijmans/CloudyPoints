# Interface
This folder contains the source code files for the Streamlit interface application

## Docker Container
To run the code in a docker container, open terminal and cd into the interface directory.
Then, run the commands below in terminal.

**Build image:**
```
docker build --platform linux/amd64 --file interface.Dockerfile -t cp-interface:latest .
```

**Run container:**
```
docker run -p 8501:8501 -e CP_BASE_URL="http://192.168.0.213:5001" cp-interface:latest
```
Change the ENV variable CP_BASE_URL to the correct url of the model serving API.
