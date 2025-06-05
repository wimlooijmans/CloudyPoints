# CICD Pipeline

A CICD pipeline is set up to check the code quality and to run an automatic deployment of the applications. GitHub Actions is used to run this CICD pipeline. The workflows are defined in .yml files in the *.github/workflows* folder.

The CICD pipeline runs every time there is a pull request or push to the develop and main branch. There is a separate file for each branch. Both these files call the *reusable-CI.yml* and *reusable-CD.yml* file, but give different names to the deployed services.

## Continuous Integration

The CI part of the pipeline consists out of two parts. First pre-commit is run to check the code quality. Next, Pytest checks if the predefined tests succeed. The complete CI pipeline is defined in *reusable-CI.yml*.

### Pre-commit
Pre-commit runs first to check the code quality. Three checks are defined:
1. Pre-commit hooks
    - check-yaml
    - end-of-file-fixer
    - trailing-whitespace
2. Ruff linter
3. Black formatter

### Pytest
If the pre-commit succeeds, Pytest is run to check the code. The test files are in the *tests/* folder in the root directory.

#### Testing Flask
Two files are related to test the flask application:
- *conftest.py*
- *test_api_model.py*

Two checks are done. First, a test is done that the home page returns a response code 200. Secondly, the */predict* route is tested by sending an image over a POST request. This test succeeds if a response code 201 is returned and the returned content-type is "image/png".

### Testing Streamlit Helper Functions
Two files are related to test the Streamlit helper functions:
- *test_streamlit_helper_functions.py*
- *filenmaes_to_city_id.json*

The file *test_streamlit_helper_functions.py* defines the test for the helper functions. Since these functions require lists as input and output, a file with data is created (*filenmaes_to_city_id.json*) to handle this more easily.

## Continuous Deployment
If the Pre-commit and Pytest checks are completed successfully, the CD pipeline will run. This workflow requires two inputs, the name for the cloud run service for respectively the Model Serving API and Interface:
1. model-serving-api-name
2. interface-name

An environment variable `MODEL_SERVING_BASE_URL` is set to store the url of the Model Serving API, based on the model-serving-api-name input. This way the interface knows which url to use to call the inference.

The workflow consists out of five steps:
1. Checkout code
2. Google authentication
3. Set up the Google Cloud SDK
4. Deploy Model Serving API to Cloud
5. Deploy Interface

For the authentication, a separate service account for GitHub Actions was created in the Google Cloud Project, using the Workload Identity Federation.

The deployment steps for the Model Serving API and Interface are discussed in *MODEL_SERVING_API.md* and *interface/INTERFACE.md*, respectively.
