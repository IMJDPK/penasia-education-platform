#!/usr/bin/env python3
"""
PythonAnywhere Auto-Deployment Script
Automatically reloads the web app after GitHub pushes using PythonAnywhere API

Usage:
    python3 deploy_via_api.py

Environment Variables:
    PA_USERNAME: PythonAnywhere username
    PA_TOKEN: PythonAnywhere API token
    WEBAPP_DOMAIN: Web app domain (default: imjdpk.pythonanywhere.com)
"""

import os
import sys
import time
import requests
from datetime import datetime

class PythonAnywhereDeployer:
    def __init__(self, username=None, token=None, domain=None):
        self.username = username or os.getenv('PA_USERNAME', 'imjdpk')
        self.token = token or os.getenv('PA_TOKEN', '77050fab193b4b5672ea7bd549988bb104e42ae0')
        self.domain = domain or os.getenv('WEBAPP_DOMAIN', 'www.penasia.edu.hk')  # Updated default domain

        self.base_url = f'https://www.pythonanywhere.com/api/v0/user/{self.username}'
        self.headers = {'Authorization': f'Token {self.token}'}

        print(f"🚀 PythonAnywhere Deployer initialized for {self.domain}")

    def check_api_connection(self):
        """Test API connection and authentication"""
        try:
            response = requests.get(f'{self.base_url}/cpu/', headers=self.headers, timeout=10)
            if response.status_code == 200:
                print("✅ API connection successful")
                return True
            else:
                print(f"❌ API authentication failed: {response.status_code}")
                print(f"Response: {response.text}")
                return False
        except Exception as e:
            print(f"❌ API connection error: {e}")
            return False

    def get_webapp_status(self):
        """Get current webapp status"""
        try:
            response = requests.get(f'{self.base_url}/webapps/', headers=self.headers, timeout=10)
            if response.status_code == 200:
                webapps = response.json()
                for app in webapps:
                    if app.get('domain_name') == self.domain:  # Changed from 'domain' to 'domain_name'
                        return app
                print(f"⚠️  Webapp {self.domain} not found")
                return None
            else:
                print(f"❌ Failed to get webapp status: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Error getting webapp status: {e}")
            return None

    def reload_webapp(self):
        """Reload the webapp"""
        print(f"🔄 Reloading webapp: {self.domain}")

        try:
            response = requests.post(
                f'{self.base_url}/webapps/{self.domain}/reload/',
                headers=self.headers,
                timeout=30
            )

            if response.status_code == 200:
                print("✅ Webapp reload initiated successfully")
                return True
            else:
                print(f"❌ Webapp reload failed: {response.status_code}")
                print(f"Response: {response.text}")
                return False

        except Exception as e:
            print(f"❌ Error reloading webapp: {e}")
            return False

    def wait_for_reload(self, max_wait=60):
        """Wait for reload to complete"""
        print(f"⏳ Waiting for reload to complete (max {max_wait}s)...")

        start_time = time.time()
        while time.time() - start_time < max_wait:
            status = self.get_webapp_status()
            if status:
                # Check if reload is complete (you might need to adjust this based on API response)
                print("✅ Reload appears to be complete")
                return True

            time.sleep(5)

        print("⚠️  Reload may still be in progress")
        return True  # Don't fail, just warn

    def deploy(self):
        """Complete deployment process"""
        print(f"🚀 Starting deployment for {self.domain}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Step 1: Check API connection
        if not self.check_api_connection():
            return False

        # Step 2: Get initial status
        initial_status = self.get_webapp_status()
        if initial_status:
            print(f"📊 Initial status: {initial_status.get('state', 'unknown')}")

        # Step 3: Reload webapp
        if not self.reload_webapp():
            return False

        # Step 4: Wait for completion
        self.wait_for_reload()

        # Step 5: Final status check
        final_status = self.get_webapp_status()
        if final_status:
            print(f"📊 Final status: {final_status.get('state', 'unknown')}")

        print("🎉 Deployment completed successfully!")
        return True

def main():
    """Main deployment function"""
    print("PythonAnywhere Auto-Deployment Script")
    print("=" * 50)

    deployer = PythonAnywhereDeployer()

    success = deployer.deploy()

    if success:
        print("\n✅ Deployment successful!")
        sys.exit(0)
    else:
        print("\n❌ Deployment failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()