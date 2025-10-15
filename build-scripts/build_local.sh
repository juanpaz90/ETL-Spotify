#!/bin/bash

TAG_j=spotify_data_extractor

docker build -t "$TAG_j" -f 'build-scripts/spotify_data.Dockerfile' .

docker run \
  --env-file .env \
  -p 8000:8000 \
  -d "$TAG_j"