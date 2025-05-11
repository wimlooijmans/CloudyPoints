from pathlib import Path

import torch
import numpy as np
import torchvision.transforms.v2 as transforms

from flask import (
    Flask,
    render_template,
    request,
    send_file,
)
from werkzeug.utils import secure_filename

from PIL import Image
from matplotlib import cm

# from cityscapes_dataset import CityscapesDataset
from model_loader import MiDaSFineTuner

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

# Paths
path_src = Path(__file__).resolve().parent
path_models = path_src.parent / "models"
path_user_data_storage = path_src.parent / "mnt" / "user_data_storage"
url_DPT_Hybrid = "https://storage.googleapis.com/cp_bucket-1/models/DPT_Hybrid_1.ckpt"
path_uploads = path_user_data_storage / "uploads"
path_outputs = path_user_data_storage / "outputs"

# create directories for uploads and outputs
if not path_uploads.exists():
    path_uploads.mkdir(parents=True)

if not path_outputs.exists():
    path_outputs.mkdir(parents=True)

# Load model
model_load = MiDaSFineTuner.load_from_checkpoint(url_DPT_Hybrid)
model_load.eval()


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# create Flask instance
def create_app():
    app = Flask(__name__)
    app.config["UPLOAD_FOLDER"] = path_uploads
    app.config["OUTPUTS_FOLDER"] = path_outputs
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

    @app.route("/")
    def welcome():
        title = "CloudyPoints"
        greeting = "Welcome to CloudyPoints Model Serving"
        return render_template("welcome.html", title=title, greeting=greeting)

    @app.route("/predict", methods=["POST"])
    def predict():
        if request.method == "POST":
            key = list(request.files.keys())[0]  # get first key
            img = request.files.get(key)
            if img and allowed_file(img.filename):
                # Save image to mounted GCS bucket
                filename = secure_filename(img.filename)
                img.save(app.config["UPLOAD_FOLDER"] / filename)

                # Convert to PIL Image and store image size
                img = Image.open(img)
                img_size = img.size

                # Transform image to tensor
                transform = transforms.Compose(
                    [
                        transforms.Resize((384, 384)),
                        transforms.ToTensor(),
                    ]
                )
                img_tensor = transform(img)
                img_tensor = torch.unsqueeze(img_tensor, dim=0)

                device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
                img = img_tensor.to(device)  # Move input tensor to the correct device
                model_load.to(device)  # Ensure the model is on the correct device

                # Inference
                with torch.no_grad():  # Disable gradient calculation
                    output = model_load(img)

                # Transform depth output to image
                depth_map = (
                    output.squeeze().cpu().numpy()
                )  # Remove batch dimension and convert to numpy array
                depth_map *= 1.0 / depth_map.max()  # scale between 0 and 1
                depth_img = Image.fromarray(np.uint8(cm.viridis(depth_map) * 255))

                # Resize and save depth output as image in mounted GCS bucket
                path_depth_img = app.config["OUTPUTS_FOLDER"] / (
                    "prediction-" + filename
                )
                depth_img.resize(img_size).save(path_depth_img, "PNG")

                return send_file(path_depth_img), 201

        return ""

    return app


app = create_app()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
