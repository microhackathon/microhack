#!/usr/bin/env python3
"""
Upload Sample Data to Google Drive

This script helps you upload the sample_data.csv file to your Google Drive.
"""

import os
import sys
from pathlib import Path
from google_drive import GoogleDriveConnector

def upload_sample_data():
    """Upload sample_data.csv to Google Drive."""
    
    # Check if credentials exist
    credentials_file = "config/credentials.json"
    if not os.path.exists(credentials_file):
        print("❌ Credentials file not found!")
        print(f"Please place your credentials.json file in the config/ directory")
        print("Run './setup.sh' first to get setup instructions")
        return False
    
    # Check if sample data exists
    sample_file = "sample_data.csv"
    if not os.path.exists(sample_file):
        print(f"❌ Sample data file not found: {sample_file}")
        return False
    
    try:
        print("🔐 Authenticating with Google Drive...")
        drive = GoogleDriveConnector(credentials_file)
        
        print(f"📤 Uploading {sample_file} to Google Drive...")
        
        # Upload the file
        file_metadata = {
            'name': sample_file,
            'parents': []  # Upload to root folder
        }
        
        # Read the file content
        with open(sample_file, 'rb') as f:
            file_content = f.read()
        
        # Create media upload
        from googleapiclient.http import MediaIoBaseUpload
        import io
        media = MediaIoBaseUpload(
            io.BytesIO(file_content),
            mimetype='text/csv',
            resumable=True
        )
        
        # Upload the file
        file = drive.service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id,name,webViewLink'
        ).execute()
        
        print(f"✅ Successfully uploaded to Google Drive!")
        print(f"📁 File ID: {file.get('id')}")
        print(f"📄 File Name: {file.get('name')}")
        print(f"🔗 View Link: {file.get('webViewLink')}")
        print(f"\n🎯 You can now use this file with your Pathway pipeline!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error uploading file: {e}")
        return False

def main():
    print("=" * 60)
    print("📤 Upload Sample Data to Google Drive")
    print("=" * 60)
    
    if upload_sample_data():
        print("\n" + "=" * 60)
        print("🎉 Upload complete! You can now run your Google Drive pipeline.")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ Upload failed. Please check the error messages above.")
        print("=" * 60)

if __name__ == "__main__":
    main() 