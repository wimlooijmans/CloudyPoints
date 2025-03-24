from pathlib import Path

import torch
import numpy as np
import torch.nn as nn
import matplotlib.pyplot as plt
from torchsummary import summary
from torch.utils.data import Dataset
from torchvision.io import read_image
from torchvision.io import ImageReadMode
from torch.utils.data import DataLoader
import torchvision.transforms.v2 as transforms
import torch.optim as optim
import torchmetrics
from torchmetrics.image import StructuralSimilarityIndexMeasure
import pytorch_lightning as pl
from pytorch_lightning import Trainer
from pytorch_lightning.callbacks import ModelCheckpoint, EarlyStopping

from flask import Flask, render_template #, request, jsonify, redirect, url_for

from PIL import Image

from cityscapes_dataset import CityscapesDataset
from model_loader import MiDaSFineTuner

# create Flask instance
app = Flask(__name__)

# Paths
path_src = Path(__file__).resolve().parent
path_models = path_src.parent / 'models'
path_DPT_Hybrid = path_models / 'DPT_Hybrid_1.ckpt'

# Load model
model_load = MiDaSFineTuner.load_from_checkpoint(path_DPT_Hybrid)

# Load sample image
sample_image = Image.open('/src/berlin_000000_000019_left_image.png')

# Transform sample image to tensor
transform = transforms.Compose([
    transforms.Resize((384, 384)),
    transforms.ToTensor(),
])

img_tensor = transform(sample_image)
img_tensor = torch.unsqueeze(img_tensor, dim=0)

# Normalization ???

@app.route('/')
def welcome():
    title = 'CloudyPoints'
    greeting = 'Welcome to CloudyPoints'
    return render_template('welcome.html', title=title, greeting=greeting)

@app.route('/predict')
def predict(img=img_tensor):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    img = img.to(device)  # Move input tensor to the correct device
    model_load.to(device)  # Ensure the model is on the correct device

    with torch.no_grad():  # Disable gradient calculation
        output = model_load(img)

    depth_map = output.squeeze().cpu().numpy()  # Remove batch dimension and convert to numpy arra
    print(type(depth_map))
    print(depth_map.shape)
    # return depth_map
    return "Prediction done"

if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=5001)
    app.run(debug=True)
