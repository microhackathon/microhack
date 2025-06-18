#!/usr/bin/env python3
"""
Google Drive Service Account Setup

This script helps you set up Google Drive access using a service account.
This is an alternative to OAuth that doesn't require user interaction.
"""

import os
import sys
from pathlib import Path

def setup_service_account():
    """Set up Google Drive access using service account."""
    
    # Check if service account key exists
    service_account_file = "config/service-account-key.json"
    
    if not os.path.exists(service_account_file):
        print("❌ Service account key file not found!")
        print(f"Please place your service account JSON key file in: {service_account_file}")
        print("\nTo create a service account:")
        print("1. Go to https://console.cloud.google.com/")
        print("2. Navigate to 'APIs & Services' > 'Credentials'")
        print("3. Click 'Create Credentials' > 'Service Account'")
        print("4. Download the JSON key file")
        print("5. Rename it to 'service-account-key.json'")
        print("6. Place it in the 'config/' directory")
        return False
    
    try:
        print("🔐 Setting up Google Drive service account access...")
        
        # Import here to avoid issues if not installed
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
        
        # Set up credentials
        SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
        credentials = service_account.Credentials.from_service_account_file(
            service_account_file, scopes=SCOPES
        )
        
        # Test the connection
        service = build('drive', 'v3', credentials=credentials)
        
        # List files to test access
        results = service.files().list(pageSize=10).execute()
        files = results.get('files', [])
        
        print("✅ Service account authentication successful!")
        print(f"Found {len(files)} files in Google Drive")
        
        if files:
            print("Sample files:")
            for file in files[:3]:
                print(f"  - {file['name']} ({file['id']})")
        
        print("\n📝 Next steps:")
        print("1. Share your Google Drive folder with the service account email")
        print("2. Update your .env file to use service account mode")
        print("3. Run your Docker containers")
        
        return True
        
    except Exception as e:
        print(f"❌ Service account setup failed: {e}")
        return False

def main():
    print("=" * 60)
    print("🔐 Google Drive Service Account Setup")
    print("=" * 60)
    
    if setup_service_account():
        print("\n" + "=" * 60)
        print("🎉 Service account setup complete!")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ Service account setup failed.")
        print("=" * 60)

if __name__ == "__main__":
    main() 