#!/bin/bash

# RA100 TensorX - DockerHub Push Script
# This script automates the process of making your application public on DockerHub.

# Exit on error
set -e

IMAGE_NAME="ra100-tensorx"

echo "------------------------------------------------"
echo "📦 DockerHub Distribution Tool"
echo "------------------------------------------------"

# 1. Ask for DockerHub Username
read -p "Enter your DockerHub Username: " DOCKER_USER

if [ -z "$DOCKER_USER" ]; then
    echo "❌ Error: Username cannot be empty."
    exit 1
fi

# 2. Build the latest image (to ensure it's up to date)
echo "Building local image: $IMAGE_NAME..."
docker build -t $IMAGE_NAME:latest .

# 3. Login to DockerHub (if not already logged in)
echo "Logging into DockerHub..."
docker login

# 4. Tag the image for your repository
echo "Tagging image as $DOCKER_USER/$IMAGE_NAME:latest..."
docker tag $IMAGE_NAME:latest $DOCKER_USER/$IMAGE_NAME:latest

# 5. Push to DockerHub
echo "Pushing to DockerHub... this may take a moment."
docker push $DOCKER_USER/$IMAGE_NAME:latest

echo "------------------------------------------------"
echo "✅ SUCCESS!"
echo "Your application is now public at: https://hub.docker.com/r/$DOCKER_USER/$IMAGE_NAME"
echo "------------------------------------------------"
