#!/bin/bash

# Deploy Spotify extractor container
deploy_sp_extractor() {
    echo " >> Spotify extractor container Deployment << "

    gcloud run jobs deploy spotify-extractor \
    --project=$PROJECT_ID \
    --image=us-east1-docker.pkg.dev/$PROJECT_ID/$REPOSITORY_NAME/$IMAGE_NAME:latest \
    --region=us-east1 \
    --cpu=1 \
    --memory=4Gi \
    --task-timeout=30m \
    --max-retries=1 \
    --set-env-vars=PROJECT_ID=$PROJECT_ID \
    --service-account=$SERVICE_ACCOUNT
}

deploy_sp_extractor

if [ $? -ne 0 ];
then 
    echo " >> Error Deploying Spotify extractor"
    exit 1
else 
    echo " >> Deploy Spotify extractor successfully"
fi