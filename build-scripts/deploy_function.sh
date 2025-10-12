#!/bin/bash

deploy_function() {
  gcloud functions deploy spotify_etl \
    --region=us-east1 \
    --memory=512MB \
    --timeout=540s \
    --source=./src \
    --trigger-topic=spotify-etl \
    --max-instances=5 \
    --runtime=python312 \
    --set-env-vars=PROJECT_ID=$PROJECT_ID \
    --service-account=etl-deploy@testing-etl-jep.iam.gserviceaccount.com \
    --build-service-account=projects/$PROJECT_ID/serviceAccounts/etl-deploy@testing-etl-jep.iam.gserviceaccount.com
}

deploy_function
