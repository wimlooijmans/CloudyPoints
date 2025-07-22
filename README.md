# CloudyPoints ☁️
CloudyPoints  - Machine Learning Systems Design Project.

## Description
CloudyPoints is a project where we'll work on Monocular Depth Estimation (MDE) and 3D Point Cloud Generation. The noun is inspired from the second part of the project. First, we need to know what is MDE. MDE is the task of predicting the depth of each pixel in an image using only a single RGB image (rather than stereo or LiDAR). The goal is to infer the 3D structure of a scene from a 2D image (using 3D point cloud).
This task is super important in real life like in Autonomous systems (Collision avoidance, ...) and video surveillance.

## GOAL of the project
The final goal of this project is to be able to design and implement an application that generates a depth image from a provided image. During the design of this system, Machine Learning Operations (MLOps) best practices will be used. The focus will be on outdoor, street scene images.

## Dataset
During this project, we will use the CityScapes Dataset which provides images of urban street scenes and depth measurements. First, we need input images, which are RGB images, representing the scene on which we want to estimate the depth and generate the 3D point cloud. Second, we need the ground truth Depth maps of our input images in order to compare with the predictions made by our model.

![RGB - Ground Truth Depth map](https://github.com/wimlooijmans/CloudyPoints/blob/8c5041ef7c8b31c287e06472e767010eb0aa7519/sample_images/RGB%20-%20Ground%20Truth%20Depth%20map.png)

<!-- ## TODO
| # | Week | Work package| status |
| --- | --- | --- | --- |
| 1.1 | W01 | Pick a team | ✅ |
| 1.2 | W02 | Select a use case | ✅ |
| 1.3 | W02 | Define the use case | ✅ |
| 1.4 | W02 | Find a cool name | ✅ |
| 1.5 | W02 | Setup communication channel | ✅ |
| 1.6 | W02 | Setup a code versioning repository | ✅ |
| 1.7 | W02 | Project card | ✅ |
| 2.1 | W03 | Prepare data and Exploratory Data Analysis (EDA) | ✅ |
| 2.2 | W03 | Cloud environment | ✅ |
| 2.3 | W04 | Train ML model | ✅ |
| 2.4 | W04 | Evaluate ML model | ✅ |
| 2.5 | W04 | Document data analysis and model performance | ✅ | -->

## Exploratory Data Analysis and Data Preparation

A Exploratory Data Analysis is done and described:
[Exploratory Data Analysis](EDA.md)

To resize the images from the Cityscapes Dataset and created the ground truth depth maps from the distance measurements, a data preparation is carried out. This is described in the
[Data Preparation](data_preparation/data_preparation.md).


## Implementation

The application consists out of two separate services
1. [The Model Serving API](MODEL_SERVING_API.md)
2. [The Streamlit Interface](interface/INTERFACE.md)

Both applications are separately deployed in Google Cloud Run.

A [CICD pipeline](CICD.md) is set up to check the code quality and automatically deploy the services.

## Team
Amar Hamouma  - amar.hamouma@student.uliege.be.\
Wim Looijmans - wim.looijmans@student.uliege.be.

## License
This work is licensed under the [MIT License](./LICENSE).
