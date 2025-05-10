import os

# Load model serving api address from env
cp_serving_base_url = os.getenv("CP_BASE_URL", "http://127.0.0.1:5001")
cp_route_predict = os.getenv("CP_ROUTE_PREDICT", "predict")
cp_serving_url = cp_serving_base_url + "/" + cp_route_predict

# Max timeout for request
# take in account start-up time for cp container
max_timeout = 180
