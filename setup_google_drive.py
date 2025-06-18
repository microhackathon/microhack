#!/usr/bin/env python3
"""
Google Drive Setup Script for MicroHack

This script helps you set up Google Drive integration for your Pathway pipeline.
"""

import os
import sys
from pathlib import Path

def print_header():
    print("=" * 60)
    print("🚀 Google Drive Setup for MicroHack")
    print("=" * 60)

def print_steps():
    print("\n📋 Setup Steps:")
    print("1. Create a Google Cloud Project")
    print("2. Enable Google Drive API")
    print("3. Create credentials")
    print("4. Download credentials file")
    print("5. Upload sample data to Google Drive")
    print("6. Test the integration")

def create_config_directory():
    """Create config directory if it doesn't exist."""
    config_dir = Path("config")
    config_dir.mkdir(exist_ok=True)
    print(f"✅ Created config directory: {config_dir}")

def check_credentials():
    """Check if credentials file exists."""
    credentials_file = Path("config/credentials.json")
    if credentials_file.exists():
        print(f"✅ Credentials file found: {credentials_file}")
        return True
    else:
        print(f"❌ Credentials file not found: {credentials_file}")
        return False

def print_google_cloud_instructions():
    print("\n🔧 Google Cloud Console Setup:")
    print("1. Go to https://console.cloud.google.com/")
    print("2. Create a new project or select existing one")
    print("3. Enable the Google Drive API:")
    print("   - Go to 'APIs & Services' > 'Library'")
    print("   - Search for 'Google Drive API'")
    print("   - Click 'Enable'")
    print("4. Create credentials:")
    print("   - Go to 'APIs & Services' > 'Credentials'")
    print("   - Click 'Create Credentials' > 'OAuth 2.0 Client IDs'")
    print("   - Choose 'Desktop application'")
    print("   - Download the JSON file")
    print("5. Rename the downloaded file to 'credentials.json'")
    print("6. Place it in the 'config/' directory")

def print_sample_data_instructions():
    print("\n📁 Sample Data Setup:")
    print("1. Upload 'sample_data.csv' to your Google Drive")
    print("2. Note the filename (default: 'sample_data.csv')")
    print("3. Make sure the file is accessible to your Google account")

def print_test_instructions():
    print("\n🧪 Testing the Integration:")
    print("1. Build the containers:")
    print("   docker compose -f google_drive.yml build")
    print("2. Run the application:")
    print("   docker compose -f google_drive.yml up")
    print("3. The app will:")
    print("   - Authenticate with Google Drive (browser will open)")
    print("   - Find and read your CSV file")
    print("   - Stream data through the Pathway pipeline")
    print("4. Check the output in 'output.csv'")

def print_environment_variables():
    print("\n⚙️ Environment Variables (for .env file):")
    print("INPUT_CONNECTOR=google_drive")
    print("GOOGLE_DRIVE_FILENAME=sample_data.csv")
    print("GOOGLE_DRIVE_REFRESH_INTERVAL=30")
    print("GOOGLE_DRIVE_VALUE_COLUMN=value")

def main():
    print_header()
    print_steps()
    
    create_config_directory()
    
    if not check_credentials():
        print_google_cloud_instructions()
    else:
        print("\n✅ Credentials are already set up!")
    
    print_sample_data_instructions()
    print_test_instructions()
    print_environment_variables()
    
    print("\n" + "=" * 60)
    print("🎉 Setup complete! Follow the instructions above to get started.")
    print("=" * 60)

if __name__ == "__main__":
    main() 