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
PATH_IMAGE_RECOMMENDATIONS="us-east1-docker.pkg.dev/$GCP_PROJECT/recommendation-job/recommendation-job:latest"

# List docker images
docker images

# Push container
echo "Push Recommendations container"
docker push "${PATH_IMAGE_RECOMMENDATIONS}"
if [ $? -ne 0 ]; then
  echo "Failed to push Recommendations image"
  exit 1
fi
echo "Recommendations image pushed successfully."
