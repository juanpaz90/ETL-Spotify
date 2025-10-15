#!/bin/bash

# LOCATION-docker.pkg.dev/PROJECT_ID/REPOSITORY_NAME/IMAGE_NAME:TAG
SPOTIFY_EXTRACTOR_TAG="us-east1-docker.pkg.dev/$PROJECT_ID/spotify-data-extractor/spotify-data-extractor:latest"

# Build spotify-data-extractor image
echo " Build spotify-data-extractor container"
docker build -t "$SPOTIFY_EXTRACTOR_TAG" -f 'build/spotify_extractor.Dockerfile' .
if [ $? -ne 0 ]; then
  echo "Error: Failed to build spotify-data-extractor image."
  exit 1
fi
echo "spotify-data-extractor image built successfully."

# List docker images
docker images
