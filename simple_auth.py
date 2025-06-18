#!/usr/bin/env python3
"""
Simple Google Drive Authentication

This script uses a simpler OAuth approach that should work better.
"""

import os
import sys
from pathlib import Path

def simple_auth():
    """Simple Google Drive authentication."""
    
    # Check if credentials exist
    credentials_file = "config/credentials.json"
    token_file = "config/token.json"
    
    if not os.path.exists(credentials_file):
        print("❌ Credentials file not found!")
        print(f"Please place your credentials.json file in the config/ directory")
        return False
    
    try:
        print("🔐 Setting up simple Google Drive authentication...")
        
        # Import required libraries
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        
        # Define scopes
        SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
        
        # Check if token already exists
        creds = None
        if os.path.exists(token_file):
            creds = Credentials.from_authorized_user_file(token_file, SCOPES)
        
        # If no valid credentials available, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                # Create flow with explicit redirect URI
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_file, 
                    SCOPES,
                    redirect_uri='urn:ietf:wg:oauth:2.0:oob'  # Use out-of-band flow
                )
                
                # Get authorization URL
                auth_url, _ = flow.authorization_url(prompt='consent')
                
                print("=" * 60)
                print("🔐 Simple Google Drive Authentication")
                print("=" * 60)
                print("1. Copy and paste this URL into your browser:")
                print(f"   {auth_url}")
                print("\n2. Sign in with your Google account")
                print("3. Grant the requested permissions")
                print("4. You'll see a page with an authorization code")
                print("5. Copy the code and paste it here")
                print("=" * 60)
                
                # Get authorization code
                auth_code = input("Enter the authorization code: ").strip()
                
                # Exchange code for credentials
                flow.fetch_token(code=auth_code)
                creds = flow.credentials
            
            # Save the credentials
            os.makedirs(os.path.dirname(token_file), exist_ok=True)
            with open(token_file, 'w') as token:
                token.write(creds.to_json())
        
        print("✅ Authentication successful!")
        print("Token saved to config/token.json")
        return True
        
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        return False

def main():
    print("=" * 60)
    print("🔐 Simple Google Drive Authentication")
    print("=" * 60)
    
    if simple_auth():
        print("\n" + "=" * 60)
        print("🎉 Authentication complete! You can now run:")
        print("   docker compose -f google_drive.yml up")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ Authentication failed.")
        print("=" * 60)

if __name__ == "__main__":
    main() 