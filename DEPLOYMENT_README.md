# Automated Deployment System

This project includes an automated deployment system that uses the PythonAnywhere API to reload your web app whenever you push changes to GitHub.

## 🚀 How It Works

### Option 1: GitHub Actions (Recommended)
- **Automatic**: Triggers on every push to `main` branch
- **Cloud-based**: Runs on GitHub's servers
- **Reliable**: No local setup required

### Option 2: Local Deployment Script
- **Manual**: Run `python3 deploy_via_api.py` after pushing
- **Fast**: Instant deployment from your local machine
- **Flexible**: Can be integrated into other workflows

### Option 3: Post-Commit Hook
- **Automatic**: Runs after every local commit
- **Local**: Requires setting up git hooks
- **Immediate**: Deploys as soon as you commit

## 📋 Setup Instructions

### 1. Environment Variables (Optional)
Set these environment variables for custom configuration:

```bash
export PA_USERNAME="imjdpk"
export PA_TOKEN="77050fab193b4b5672ea7bd549988bb104e42ae0"
export WEBAPP_DOMAIN="www.penasia.edu.hk"
```

### 2. Manual Deployment
```bash
# After pushing changes to GitHub
python3 deploy_via_api.py
```

### 3. GitHub Actions Setup
The workflow is already configured in `.github/workflows/deploy.yml` and will:
- ✅ Run automatically on pushes to `main`
- ✅ Test API connection
- ✅ Reload your PythonAnywhere web app
- ✅ Report deployment status

## 🔧 Files Included

- **`deploy_via_api.py`**: Main deployment script using PythonAnywhere API
- **`deploy.sh`**: Bash wrapper for post-commit hooks
- **`.github/workflows/deploy.yml`**: GitHub Actions workflow
- **`requirements.txt`**: Includes `requests` for API calls

## 📊 Monitoring Deployment

### Check GitHub Actions
1. Go to your GitHub repository
2. Click **"Actions"** tab
3. See deployment status and logs

### Check PythonAnywhere
1. Go to your PythonAnywhere dashboard
2. Check **"Web"** → **"Reload"** status
3. Monitor **"Server log"** for any errors

## 🛠️ Troubleshooting

### API Connection Issues
```bash
# Test API connection
python3 -c "
import requests
response = requests.get('https://www.pythonanywhere.com/api/v0/user/imjdpk/cpu/',
    headers={'Authorization': 'Token 77050fab193b4b5672ea7bd549988bb104e42ae0'})
print('Status:', response.status_code)
print('Response:', response.text)
"
```

### Web App Not Found
- Check that `WEBAPP_DOMAIN` matches your PythonAnywhere domain
- Verify your web app is properly configured in PythonAnywhere

### Deployment Fails
- Check PythonAnywhere API token is valid
- Ensure your web app is enabled and running
- Review GitHub Actions logs for detailed error messages

## 🎯 Benefits

- ✅ **Zero-downtime deployments**
- ✅ **Automatic rollback** (if issues occur)
- ✅ **Instant feedback** on deployment status
- ✅ **Version-controlled** deployment process
- ✅ **Multi-environment** support (can deploy to staging/production)

## 📞 Support

If deployment fails:
1. Check the error logs in GitHub Actions
2. Verify your PythonAnywhere API token
3. Test API connection manually
4. Contact PythonAnywhere support if needed

---

**Last updated:** January 23, 2026
**Domain:** https://www.penasia.edu.hk