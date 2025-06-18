#!/usr/bin/env python3
"""
Google Drive Authentication Setup

This script handles Google Drive authentication outside of Docker containers.
Run this first to set up authentication, then run your Docker containers.
"""

import os
import sys
from pathlib import Path

def setup_authentication():
    """Set up Google Drive authentication."""
    
    # Check if credentials exist
    credentials_file = "config/credentials.json"
    token_file = "config/token.json"
    
    if not os.path.exists(credentials_file):
        print("❌ Credentials file not found!")
        print(f"Please place your credentials.json file in the config/ directory")
        print("Run './setup.sh' first to get setup instructions")
        return False
    
    # Check if token already exists
    if os.path.exists(token_file):
        print("✅ Authentication token already exists!")
        print("You can now run your Docker containers.")
        return True
    
    try:
        print("🔐 Setting up Google Drive authentication...")
        
        # Import here to avoid issues if not installed
        from microhack.google_drive import GoogleDriveConnector
        
        # This will trigger the authentication flow
        drive = GoogleDriveConnector(credentials_file, token_file)
        
        print("✅ Authentication successful!")
        print("Token saved to config/token.json")
        print("You can now run your Docker containers.")
        
        return True
        
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        return False

def main():
    print("=" * 60)
    print("🔐 Google Drive Authentication Setup")
    print("=" * 60)
    
    if setup_authentication():
        print("\n" + "=" * 60)
        print("🎉 Authentication complete! You can now run:")
        print("   docker compose -f google_drive.yml up")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ Authentication failed. Please check the error messages above.")
        print("=" * 60)

if __name__ == "__main__":
    main() 