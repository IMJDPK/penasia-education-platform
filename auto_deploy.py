#!/usr/bin/env python3
"""
PythonAnywhere Auto-Deploy Script
Automatically pulls latest code from GitHub and updates the live site
"""

import requests
import time
import sys

# Configuration
USERNAME = 'imjdpk'
API_TOKEN = '77050fab193b4b5672ea7bd549988bb104e42ae0'
DOMAIN = 'imjdpk.pythonanywhere.com'
PROJECT_PATH = '/home/imjdpk/mysite'

BASE_URL = 'https://www.pythonanywhere.com/api/v0'
HEADERS = {'Authorization': f'Token {API_TOKEN}'}

def print_step(message):
    """Print a formatted step message"""
    print(f"\n{'='*60}")
    print(f"🔧 {message}")
    print(f"{'='*60}")

def run_console_command(command, description):
    """Execute a command in a PythonAnywhere console"""
    print(f"\n📡 {description}...")
    
    # Get or create a console
    consoles_url = f'{BASE_URL}/user/{USERNAME}/consoles/'
    response = requests.get(consoles_url, headers=HEADERS)
    
    if response.status_code != 200:
        print(f"❌ Failed to get consoles: {response.status_code}")
        return False
    
    consoles = response.json()
    
    # Use existing console or create new one
    console_id = None
    if consoles:
        console_id = consoles[0]['id']
        print(f"   Using existing console: {console_id}")
    else:
        # Create new console
        create_url = f'{BASE_URL}/user/{USERNAME}/consoles/'
        response = requests.post(
            create_url,
            headers=HEADERS,
            json={'executable': 'bash', 'arguments': []}
        )
        if response.status_code == 201:
            console_id = response.json()['id']
            print(f"   Created new console: {console_id}")
            time.sleep(2)  # Wait for console to initialize
        else:
            print(f"❌ Failed to create console: {response.status_code}")
            return False
    
    # Send command to console
    input_url = f'{BASE_URL}/user/{USERNAME}/consoles/{console_id}/send_input/'
    response = requests.post(
        input_url,
        headers=HEADERS,
        json={'input': command + '\n'}
    )
    
    if response.status_code == 200:
        print(f"   ✅ Command executed: {command}")
        time.sleep(1)  # Wait for command to execute
        return True
    else:
        print(f"   ❌ Failed to execute command: {response.status_code}")
        return False

def reload_webapp():
    """Reload the web application"""
    print(f"\n🔄 Reloading webapp...")
    
    reload_url = f'{BASE_URL}/user/{USERNAME}/webapps/{DOMAIN}/reload/'
    response = requests.post(reload_url, headers=HEADERS)
    
    if response.status_code == 200:
        print(f"   ✅ Webapp reloaded successfully!")
        return True
    else:
        print(f"   ❌ Failed to reload webapp: {response.status_code}")
        print(f"   Response: {response.content}")
        return False

def main():
    """Main deployment process"""
    print("\n" + "="*60)
    print("🚀 PYTHONANYWHERE AUTO-DEPLOYMENT STARTING")
    print("="*60)
    
    # Step 1: Pull latest code from GitHub
    print_step("Step 1: Pulling latest code from GitHub")
    commands = [
        f"cd {PROJECT_PATH}",
        "git pull origin main"
    ]
    
    for cmd in commands:
        if not run_console_command(cmd, f"Running: {cmd}"):
            print("\n❌ Deployment failed during git pull")
            sys.exit(1)
    
    # Step 2: Clear Python cache
    print_step("Step 2: Clearing Python cache")
    cache_commands = [
        f"cd {PROJECT_PATH}",
        "find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true",
        "find . -name '*.pyc' -delete 2>/dev/null || true"
    ]
    
    for cmd in cache_commands:
        run_console_command(cmd, f"Running: {cmd}")
    
    # Step 3: Update database
    print_step("Step 3: Updating database")
    db_commands = [
        f"cd {PROJECT_PATH}",
        "source venv/bin/activate",
        "python -c 'from app import app, db; app.app_context().push(); db.create_all()'"
    ]
    
    for cmd in db_commands:
        run_console_command(cmd, f"Running: {cmd}")
    
    # Step 4: Reload webapp
    print_step("Step 4: Reloading web application")
    if not reload_webapp():
        print("\n❌ Deployment completed but webapp reload failed")
        print("💡 Please manually reload via PythonAnywhere dashboard")
        sys.exit(1)
    
    # Success!
    print("\n" + "="*60)
    print("✅ DEPLOYMENT COMPLETED SUCCESSFULLY!")
    print("="*60)
    print(f"\n🌐 Your site is live at: https://{DOMAIN}")
    print("\n💡 Next steps:")
    print("   1. Wait 10-15 seconds for changes to propagate")
    print("   2. Hard refresh your browser (Ctrl+Shift+R)")
    print("   3. Verify changes at https://{DOMAIN}")
    print("\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Deployment cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Deployment failed with error: {e}")
        sys.exit(1)
