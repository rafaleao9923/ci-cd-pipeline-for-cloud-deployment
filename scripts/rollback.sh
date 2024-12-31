#!/bin/bash

# Exit on any error
set -e

# Check if version is provided
if [ -z "$1" ]; then
    echo "Error: Version not provided"
    echo "Usage: ./rollback.sh <version>"
    exit 1
fi

# Variables
NAMESPACE="production"
RELEASE_NAME="app"
VERSION=$1

# Rollback deployment
echo "Rolling back to version: $VERSION"
kubectl set image deployment/$RELEASE_NAME \
  web-app=${REGISTRY_URL}/app:$VERSION \
  -n $NAMESPACE

# Wait for rollback to complete
kubectl rollout status deployment/$RELEASE_NAME -n $NAMESPACE

# Verify rollback
echo "Rollback Status:"
kubectl get pods -n $NAMESPACE
kubectl describe deployment $RELEASE_NAME -n $NAMESPACE
