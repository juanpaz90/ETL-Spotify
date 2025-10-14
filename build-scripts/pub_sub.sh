#!/bin/bash

TOPIC_ID="spotify_etl_start_topic"
SUBSCRIPTION_ID="spotify_etl_start_subs"

create_topic() {
  gcloud pubsub topics create $TOPIC_ID
}

create_subs() {
  gcloud pubsub subscriptions create $SUBSCRIPTION_ID --topic=$TOPIC_ID
}

create_topic
create_subs