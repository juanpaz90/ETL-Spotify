#!/bin/bash

deploy_function() {
  gcloud functions deploy spotify_etl \
    --trigger-topic=spotify-etlg\
    --no-gen2 \
    --no-allow-unauthenticated
    --region=us-east1 \
    --source=./src \
    --runtime=python312 \
    --max-instances=2 \
    --timeout=300s \
    --memory=512MB \
    --set-env-vars=PROJECT_ID=$PROJECT_ID
    --service-account=etl-run-task@testing-etl-jep.iam.gserviceaccount.com
}

deploy_function
