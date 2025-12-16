# Kana Classifier v2

A deep learning project for classifying Japanese Kana characters using Convolutional Neural Networks (CNN).

## Overview

This project implements a CNN-based image classifier to recognize 6 different Japanese Kana characters: **shi (し)**, **tsu (つ)**, **n (ん)**, **so (そ)**, **no (の)**, and **me (め)**.

## Features

- Image preprocessing and normalization
- Multi-threaded dataset loading for improved performance
- CNN model with 2 convolutional layers
- Training visualization (accuracy and loss curves)
- Confusion matrix for model evaluation
- Model persistence (saved as HDF5 format)

## Requirements

```
tensorflow
opencv-python
numpy
pandas
matplotlib
seaborn
scikit-learn
tqdm
```

## Dataset Structure

```
Datasets/
├── shi/
│   └── *.png
├── tsu/
│   └── *.png
├── n/
│   └── *.png
├── so/
│   └── *.png
├── no/
│   └── *.png
└── me/
    └── *.png
```

## Model Architecture

- Input: 64x64 grayscale images
- Conv2D (32 filters, 3x3) + ReLU
- MaxPooling2D (2x2)
- Conv2D (64 filters, 3x3) + ReLU
- MaxPooling2D (2x2)
- Flatten
- Dense (128 units) + ReLU
- Dense (6 units) + Softmax

## Usage

1. Prepare your dataset in the required structure
2. Run the notebook cells sequentially
3. The trained model will be saved to `model/kana_classifier.h5`

## Training

- Train/Test split: 80/20
- Optimizer: Adam
- Loss function: Sparse Categorical Crossentropy
- Batch size: 32
- Epochs: 5

## Output

The model generates:
- Training and validation accuracy/loss plots
- Confusion matrix visualization
- Saved model file for future predictions
