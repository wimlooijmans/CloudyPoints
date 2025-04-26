from pathlib import Path
import base64
import io

import torch
import numpy as np
import torchvision.transforms.v2 as transforms

from flask import Flask, render_template , request, flash, jsonify, redirect, url_for, send_file
from werkzeug.utils import secure_filename
import requests

from PIL import Image
from matplotlib import cm

# from cityscapes_dataset import CityscapesDataset
from model_loader import MiDaSFineTuner

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Paths
path_src = Path(__file__).resolve().parent
path_models = path_src.parent / 'models'
path_user_data_storage = path_src.parent / 'mnt' / 'user_data_storage'
url_DPT_Hybrid = "https://storage.googleapis.com/cp_bucket-1/models/DPT_Hybrid_1.ckpt"
path_uploads = path_user_data_storage / 'uploads'
path_outputs = path_user_data_storage / 'outputs'

# create directories for uploads and outputs
if not path_uploads.exists():
    path_uploads.mkdir(parents=True)

if not path_outputs.exists():
    path_outputs.mkdir(parents=True)

# Load model
model_load = MiDaSFineTuner.load_from_checkpoint(url_DPT_Hybrid)
model_load.eval()

def make_prediction(img):
    """
    Input: PIL.Image
    Output: depth map PIL.Image
    """
    # Transform sample image to tensor
    transform = transforms.Compose([
        transforms.Resize((384, 384)),
        transforms.ToTensor(),
    ])
    img_tensor = transform(img)
    img_tensor = torch.unsqueeze(img_tensor, dim=0)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    img = img_tensor.to(device)  # Move input tensor to the correct device
    model_load.to(device)  # Ensure the model is on the correct device

    with torch.no_grad():  # Disable gradient calculation
        output = model_load(img)

    depth_map = output.squeeze().cpu().numpy()  # Remove batch dimension and convert to numpy array

    depth_map *= (1.0/depth_map.max()) # scale between 0 and 1
    depth_img = Image.fromarray(np.uint8(cm.viridis(depth_map)*255))
    
    return depth_img


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# create Flask instance
def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = path_uploads
    app.config['OUTPUTS_FOLDER'] = path_outputs
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

    @app.route('/')
    def welcome():
        title = 'CloudyPoints'
        greeting = 'Welcome to CloudyPoints'
        return render_template('welcome.html', title=title, greeting=greeting)


    @app.route('/upload', methods=['GET', 'POST'])
    def upload_image():
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                return redirect(url_for('direct_upload_image'), code=307)
        return '''
        <!doctype html>
        <title>Upload new Image</title>
        <h1>Upload new Image</h1>
        <form method=post enctype=multipart/form-data>
        <input type=file name=file>
        <input type=submit value=Upload>
        </form>
        '''

    @app.route('/direct_upload', methods=['POST'])
    def direct_upload_image():
        if request.method == 'POST':
            key = list(request.files.keys())[0] # get first key
            img = request.files.get(key)
            if img and allowed_file(img.filename):
                filename = secure_filename(img.filename)
                img.save(app.config['UPLOAD_FOLDER'] / filename)
                return redirect(url_for('predict'), code=307)
            
        return ""


    @app.route('/predict/', methods=['POST'])
    def predict():
        if request.method == 'POST':
            key = list(request.files.keys())[0] # get first key
            img = request.files.get(key)
            if img and allowed_file(img.filename):
                filename = secure_filename(img.filename)           
                img_upload = Image.open(img)

                depth_img = make_prediction(img_upload)
                path_depth_img = app.config['OUTPUTS_FOLDER'] / ('prediction-' + filename)
                depth_img.save(path_depth_img, "PNG")

                return redirect(url_for('show_result', img_name=filename))

                # data_depth = io.BytesIO()
                # depth_img.convert('RGB').save(data_depth, "JPEG")
                # return send_file(data_depth, mimetype='image/jpeg')
            
        return ""

    @app.route('/result/<img_name>', methods=['GET'])
    def show_result(img_name):
        if request.method == 'GET':
            path_img = app.config['UPLOAD_FOLDER'] / img_name
            img = Image.open(path_img)
            img_size = img.size

            path_depth_img = app.config['OUTPUTS_FOLDER'] / ('prediction-' + path_img.stem + '.png')
            depth_img = Image.open(path_depth_img).convert('RGB').resize(img_size)

        # encode image
        data = io.BytesIO()
        img.save(data, "JPEG")
        encoded_img_data = base64.b64encode(data.getvalue())

        # Encode depth map
        data_depth = io.BytesIO()
        depth_img.save(data_depth, "JPEG")
        encoded_depth = base64.b64encode(data_depth.getvalue())

        return render_template('result.html', title=img_name, img_data=encoded_img_data.decode('utf-8'), depth_data=encoded_depth.decode('utf-8'))

    return app

app = create_app()
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)
    # app.run(debug=True)
