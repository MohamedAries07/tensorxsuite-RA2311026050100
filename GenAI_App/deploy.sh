#!/bin/bash

# DeepCareX Deployment Script
# This script builds and runs the Explainable AI application container.

# Exit on error
set -e

IMAGE_NAME="ra100-tensorx"
CONTAINER_NAME="tensorx-service"
PORT=5000

echo "------------------------------------------------"
echo "🚀 RA100: Building TensorX Container"
echo "------------------------------------------------"

# Check if a container with the same name is already running
if [ "$(docker ps -aq -f name=$CONTAINER_NAME)" ]; then
    echo "Stopping and removing existing container..."
    docker stop $CONTAINER_NAME || true
    docker rm $CONTAINER_NAME || true
fi

# Build the image
echo "Building Docker Image: $IMAGE_NAME:latest"
docker build -t $IMAGE_NAME:latest .

echo "------------------------------------------------"
echo "🌐 Starting Local Service"
echo "------------------------------------------------"

# Check if .env file exists
if [ -f .env ]; then
    echo "✅ Using .env file for GROQ_API_KEY."
    docker run -d -p $PORT:5000 --env-file .env --name $CONTAINER_NAME $IMAGE_NAME:latest
else
    echo "⚠️  WARNING: .env file not found."
    echo "Please ensure GROQ_API_KEY is set in your environment or provide it now."
    read -p "Enter GROQ_API_KEY (or leave blank to skip): " USER_KEY
    if [ ! -z "$USER_KEY" ]; then
        docker run -d -p $PORT:5000 -e GROQ_API_KEY=$USER_KEY --name $CONTAINER_NAME $IMAGE_NAME:latest
    else
        docker run -d -p $PORT:5000 --name $CONTAINER_NAME $IMAGE_NAME:latest
    fi
fi

echo ""
echo "✨ Application is live at: http://localhost:$PORT"
echo "------------------------------------------------"
echo "📦 PUBLIC DISTRIBUTION INSTRUCTIONS"
echo "------------------------------------------------"
echo "1. GitHub: "
echo "   git init"
echo "   git add ."
echo "   git commit -m 'Initial release of DeepCareX Explainable AI'"
echo "   git remote add origin https://github.com/YOUR_USERNAME/DeepCareX.git"
echo "   git push -u origin main"
echo ""
echo "2. DockerHub: "
echo "   docker tag $IMAGE_NAME:latest YOUR_DOCKERHUB_USERNAME/$IMAGE_NAME:latest"
echo "   docker push YOUR_DOCKERHUB_USERNAME/$IMAGE_NAME:latest"
echo "------------------------------------------------"
