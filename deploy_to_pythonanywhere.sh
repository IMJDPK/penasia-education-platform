#!/bin/bash
# PythonAnywhere Auto-Deploy Script
# Updates your live site after pushing to GitHub

# Configuration - UPDATE THESE VALUES
PYTHONANYWHERE_USERNAME="your_username"
PYTHONANYWHERE_DOMAIN="your_username.pythonanywhere.com"
PYTHONANYWHERE_API_TOKEN="your_api_token_here"

echo "🚀 Deploying to PythonAnywhere..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check if changes are pushed to GitHub
if ! git diff --quiet @{u}; then
    echo "⚠️  Warning: Local changes not pushed to GitHub"
    echo "   Run 'git push origin main' first"
    exit 1
fi

echo "✓ Git is up to date"

# Trigger webapp reload via API
echo "📡 Reloading webapp on PythonAnywhere..."

RELOAD_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST \
  -H "Authorization: Token $PYTHONANYWHERE_API_TOKEN" \
  "https://www.pythonanywhere.com/api/v0/user/$PYTHONANYWHERE_USERNAME/webapps/$PYTHONANYWHERE_DOMAIN/reload/")

HTTP_CODE=$(echo "$RELOAD_RESPONSE" | tail -n1)
RESPONSE_BODY=$(echo "$RELOAD_RESPONSE" | head -n-1)

if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ Webapp reloaded successfully!"
    echo ""
    echo "🌐 Your site is now live at: https://$PYTHONANYWHERE_DOMAIN"
    echo ""
    echo "📋 Next steps on PythonAnywhere (if new models added):"
    echo "   1. Open a Bash console at pythonanywhere.com"
    echo "   2. Run: cd ~/penasia-education-platform && git pull"
    echo "   3. Run: source venv/bin/activate"
    echo "   4. Run: python -c 'from app import app, db; app.app_context().push(); db.create_all()'"
    echo ""
else
    echo "❌ Reload failed with HTTP $HTTP_CODE"
    echo "Response: $RESPONSE_BODY"
    echo ""
    echo "💡 Troubleshooting:"
    echo "   - Check your API token is correct"
    echo "   - Verify username and domain in this script"
    echo "   - Get your API token: https://www.pythonanywhere.com/user/$PYTHONANYWHERE_USERNAME/account/#api_token"
    exit 1
fi
