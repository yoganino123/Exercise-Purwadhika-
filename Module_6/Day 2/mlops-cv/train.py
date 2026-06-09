import tensorflow as tf
from tensorflow import keras
import numpy as np
import os
from model import ImageClassifier

def download_and_prepare_data():
    """Download CIFAR-10 dataset"""
    print("Downloading CIFAR-10 dataset...")
    
    # Load CIFAR-10 dataset
    (x_train, y_train), (x_test, y_test) = keras.datasets.cifar10.load_data()
    
    # Normalize pixel values
    x_train = x_train.astype('float32') / 255.0
    x_test = x_test.astype('float32') / 255.0
    
    # Resize images to 224x224 for consistency with our model
    x_train_resized = []
    x_test_resized = []
    
    print("Resizing training images...")
    for i in range(len(x_train)):
        img = tf.image.resize(x_train[i], [224, 224])
        x_train_resized.append(img.numpy())
    
    print("Resizing test images...")
    for i in range(len(x_test)):
        img = tf.image.resize(x_test[i], [224, 224])
        x_test_resized.append(img.numpy())
    
    x_train = np.array(x_train_resized)
    x_test = np.array(x_test_resized)
    
    return (x_train, y_train), (x_test, y_test)

def train_model():
    """Train the image classification model"""
    print("Starting model training...")
    
    # Create models directory
    os.makedirs("models", exist_ok=True)
    
    # Create model instance
    classifier = ImageClassifier()
    model = classifier.model
    
    # Download and prepare data
    (x_train, y_train), (x_test, y_test) = download_and_prepare_data()
    
    print(f"Training data shape: {x_train.shape}")
    print(f"Training labels shape: {y_train.shape}")
    print(f"Test data shape: {x_test.shape}")
    print(f"Test labels shape: {y_test.shape}")
    
    # Train the model
    print("Training model...")
    history = model.fit(
        x_train, y_train,
        batch_size=32,
        epochs=5,  # Keep it simple for demo
        validation_data=(x_test, y_test),
        verbose=1
    )
    
    # Save the model
    model_path = "models/cifar10_model.h5"
    model.save(model_path)
    print(f"Model saved to {model_path}")
    
    # Evaluate the model
    test_loss, test_acc = model.evaluate(x_test, y_test, verbose=0)
    print(f"Test accuracy: {test_acc:.4f}")
    
    return history

if __name__ == "__main__":
    train_model()
