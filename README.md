# CloudyPoints
CloudyPoints  - Machine Learning Systems Design Project. 

## Description 
CloudyPoints is a project where we'll work on Moncular Depth Estimation (MDE) and 3D Point Cloud Generation. The noun is inspired from the second part of the project. First, we need to know what is MDE. MDE is the task of predicting the depth of each pixel in an image using only a single RGB image (rather than stereo or LiDAR). The goal is to infer the 3D structure of a scene from a 2D image (using 3D point cloud).
This task is super important in real life like in Autonoumous systems (Collision avoidance, ...)  and video surveillance.

## GOAL of the project
The final goal of this project is to be able to design and implement the application we described in the Discription. TO do this, we need several steps as we want to design a full system using Machine Learning Operations best practices (MLOps). We will focus more on outdoor scenes.

## Dataset
During this project, we will use the CityScapes Dataset which focuses on semantic understanding of urban street scenes. We have two important kind of images. 
First, we need our input images which are RGB images representing the scence on which we want to estimate the depth and generate the 3D point cloud. Second, we need the ground truth Depth maps of our input images in order to compare with the predictions made by our model.
