#!/bin/bash

set -e

rm -rf gcp_credentials.json
cat <<EOF >>gcp_credentials.json
$GOOGLE_APPLICATION_CREDENTIALS
EOF


gcloud auth activate-service-account --key-file=gcp_credentials.json
gcloud config set project $PROJECT_ID


cleanup() {
  rm gcp_credentials.json
}

trap cleanup EXIT
