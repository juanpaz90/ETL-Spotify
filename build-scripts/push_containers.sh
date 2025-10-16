#!/bin/bash
# LOCATION-docker.pkg.dev/GCP_PROJECT/REPOSITORY_NAME/IMAGE_NAME:TAG
# GCP_PROJECT = PROJECT_ID

# Authenticate Docker to Artifact Registry
gcloud auth configure-docker us-east1-docker.pkg.dev
if [ $? -ne 0 ]; then
  echo "Error: Failed to authenticate Docker with Artifact Registry"
  exit 1
fi
echo "Docker authenticated successfully."

# Artifact Registry Image Paths
PATH_IMAGE_SPOTIFY_EXTRACTOR="us-east1-docker.pkg.dev/$PROJECT_ID/$REPOSITORY_NAME/$IMAGE_NAME:latest"

# List docker images
docker images

# Push container
echo "Push spotify-data-extractor container"
docker push "${PATH_IMAGE_SPOTIFY_EXTRACTOR}"
if [ $? -ne 0 ]; then
  echo "Failed to push spotify-data-extractor image"
  exit 1
fi
echo "spotify-data-extractor image pushed successfully."
