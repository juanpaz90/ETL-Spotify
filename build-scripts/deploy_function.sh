#!/bin/bash

deploy_function() {
  gcloud functions deploy spotify_to_bq \
    --region=us-east1 \
    --memory=1Gi \
    --timeout=540s \
    --source=./src/CloudRunFunction \
    --trigger-bucket=spotify-api-data-files \
    --max-instances=5 \
    --runtime=python312 \
    --set-env-vars=PROJECT_ID=$PROJECT_ID \
    --service-account=$SERVICE_ACCOUNT
}

deploy_function
