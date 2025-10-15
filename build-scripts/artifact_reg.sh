#!/bin/bash

# Enable Artifact Registry API
gcloud services enable artifactregistry.googleapis.com

# Check if the repositories exist or not
check_repository() {
    local repo_name=$1
    local repo_description=$2

    echo "Checking repositories..."
    if gcloud artifacts repositories describe "$repo_name" --location=us-east1 > /dev/null 2>&1; then
        echo "Repository '$repo_name' already exists. Skipping creation."
    else
        echo "Repository '$repo_name' does not exist. Creating it..."
        gcloud artifacts repositories create $repo_name \
            --repository-format=docker \
            --location=us-east1 \
            --description="$repo_description"
    fi
}

# Execute function
check_repository "spotify-data-extractor" "The repo name says everything"
