#!/bin/bash

# Exit on any error
set -e

# Variables
NAMESPACE="production"
RELEASE_NAME="app"

# Create namespace if it doesn't exist
kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

# Add Helm repositories
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update

# Update Helm dependencies
helm dependency update ../helm

# Deploy application using Helm
helm upgrade --install $RELEASE_NAME ../helm \
  --namespace $NAMESPACE \
  --set image.tag=${IMAGE_TAG:-latest} \
  --values ../helm/values.yaml

# Wait for deployment to complete
kubectl rollout status deployment/$RELEASE_NAME -n $NAMESPACE

# Display deployment status
echo "Deployment Status:"
kubectl get pods,services,ingress -n $NAMESPACE
