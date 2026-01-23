#!/bin/bash
# Post-commit deployment hook for PythonAnywhere
# This script runs after successful git push to automatically deploy

echo "🚀 Starting post-commit deployment..."

# Check if we're on main branch
BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$BRANCH" != "main" ]; then
    echo "Not on main branch, skipping deployment"
    exit 0
fi

# Run the deployment script
python3 deploy_via_api.py

if [ $? -eq 0 ]; then
    echo "✅ Deployment completed successfully!"
    echo "🌐 Your site should be updated at: https://www.penasia.edu.hk"
else
    echo "❌ Deployment failed!"
    exit 1
fi