#!/bin/bash

deploy_function() {
  gcloud functions deploy spotify_etl \
    --trigger-topic=spotify-etlg\
    --no-allow-unauthenticated \
    --region=us-east1 \
    --source=./src \
    --runtime=python312 \
    --max-instances=5 \
    --timeout=540s \
    --memory=512MB \
    --set-env-vars=PROJECT_ID=$PROJECT_ID \
    --service-account=etl-deploy@testing-etl-jep.iam.gserviceaccount.com \
    --build-service-account=projects/$PROJECT_ID/serviceAccounts/etl-deploy@testing-etl-jep.iam.gserviceaccount.com
}

deploy_function
