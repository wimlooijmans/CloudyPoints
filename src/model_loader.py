from pathlib import Path

import torch
# import numpy as np
import torch.nn as nn
# import matplotlib.pyplot as plt
# from torchsummary import summary
# from torch.utils.data import Dataset
# from torchvision.io import read_image
# from torchvision.io import ImageReadMode
# from torch.utils.data import DataLoader
# import torchvision.transforms.v2 as transforms
import torch.optim as optim
# import torchmetrics
from torchmetrics.image import StructuralSimilarityIndexMeasure
import pytorch_lightning as pl
# from pytorch_lightning import Trainer
# from pytorch_lightning.callbacks import ModelCheckpoint, EarlyStopping

class MiDaSFineTuner(pl.LightningModule):
    def __init__(self, learning_rate=5e-5):
        super().__init__()
        self.model = torch.hub.load("intel-isl/MiDaS", "DPT_Hybrid")
        self.learning_rate = learning_rate
        self.lossa_fn = nn.L1Loss()


        self.train_ssi = StructuralSimilarityIndexMeasure(data_range=1.0)
        self.val_ssi = StructuralSimilarityIndexMeasure(data_range=1.0)
        self.test_ssi = StructuralSimilarityIndexMeasure(data_range=1.0)

        for param in self.model.parameters():
          param.requires_grad = True

        for param in self.model.scratch.output_conv.parameters():
          param.requires_grad = True

    def forward(self, x):
        return self.model(x)

    def training_step(self, batch, batch_idx):
        x, y = batch
        y = y / 255
        y_hat = self(x)
        y_hat = (y_hat - y_hat.min()) / (y_hat.max() - y_hat.min())

        y_hat = y_hat.unsqueeze(1)
        #visualize_prediction(x, y_hat, y)
        loss = self.loss_fn(y_hat, y)

        train_ssi = self.train_ssi(y_hat, y)

        self.log("train_loss", loss, on_step=True, on_epoch=True, prog_bar=True, logger=True)
        self.log("train_ssi", train_ssi, on_step=False, on_epoch=True, prog_bar=True, logger=True)

        return loss

    def on_train_epoch_end(self):
        self.train_ssi.reset()

    def validation_step(self, batch, batch_idx):
        x, y = batch
        y = y / 255
        y_hat = self(x)
        y_hat = (y_hat - y_hat.min()) / (y_hat.max() - y_hat.min())

        y_hat = y_hat.unsqueeze(1)
        #visualize_prediction(x, y_hat, y)

        loss = self.loss_fn(y_hat, y)
        val_ssi = self.val_ssi(y_hat, y)

        self.log("val_loss", loss, on_step=False, on_epoch=True, prog_bar=True, logger=True)
        self.log("val_ssi", val_ssi, on_step=False, on_epoch=True, prog_bar=True, logger=True)

        return loss

    def on_validation_epoch_end(self):
        self.val_ssi.reset()


    def test_step(self, batch, batch_idx):
        x, y = batch

        y = y / 255
        y_hat = self(x)
        y_hat = (y_hat - y_hat.min()) / (y_hat.max() - y_hat.min())

        y_hat = y_hat.unsqueeze(1)

        #visualize_prediction(x, y_hat, y)

        loss = self.loss_fn(y_hat, y)
        test_ssi = self.test_ssi(y_hat, y)

        self.log("test_loss", loss, on_step=False, on_epoch=True, prog_bar=True, logger=True)
        self.log("test_ssi", test_ssi, on_step=False, on_epoch=True, prog_bar=True, logger=True)

        return loss

    def on_test_epoch_end(self):
        self.test_ssi.reset()

    def configure_optimizers(self):
        optimizer = optim.Adam(self.parameters(), lr=self.learning_rate)
        return optimizer