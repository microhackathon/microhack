import os
import json
import pandas as pd
from typing import List, Dict, Any, Optional
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io
import time

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

class GoogleDriveConnector:
    def __init__(self, credentials_file: str = "config/credentials.json", token_file: str = "config/token.json"):
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.service = None
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Google Drive API."""
        creds = None
        
        # The file token.json stores the user's access and refresh tokens.
        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_file(self.token_file, SCOPES)
        
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_file):
                    raise FileNotFoundError(
                        f"Credentials file not found: {self.credentials_file}\n"
                        "Please download credentials.json from Google Cloud Console and place it in the config/ directory."
                    )
                
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_file, SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save the credentials for the next run
            os.makedirs(os.path.dirname(self.token_file), exist_ok=True)
            with open(self.token_file, 'w') as token:
                token.write(creds.to_json())
        
        self.service = build('drive', 'v3', credentials=creds)
    
    def list_files(self, query: str = None) -> List[Dict[str, Any]]:
        """List files in Google Drive."""
        try:
            results = self.service.files().list(
                pageSize=100,
                fields="nextPageToken, files(id, name, mimeType, modifiedTime)",
                q=query
            ).execute()
            
            return results.get('files', [])
        except Exception as e:
            print(f"Error listing files: {e}")
            return []
    
    def download_file(self, file_id: str) -> Optional[bytes]:
        """Download a file from Google Drive."""
        try:
            request = self.service.files().get_media(fileId=file_id)
            file = io.BytesIO()
            downloader = MediaIoBaseDownload(file, request)
            
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(f"Download {int(status.progress() * 100)}%")
            
            return file.getvalue()
        except Exception as e:
            print(f"Error downloading file {file_id}: {e}")
            return None
    
    def read_csv_from_drive(self, file_id: str) -> Optional[pd.DataFrame]:
        """Read a CSV file from Google Drive."""
        file_content = self.download_file(file_id)
        if file_content:
            try:
                return pd.read_csv(io.BytesIO(file_content))
            except Exception as e:
                print(f"Error reading CSV: {e}")
                return None
        return None
    
    def read_excel_from_drive(self, file_id: str) -> Optional[pd.DataFrame]:
        """Read an Excel file from Google Drive."""
        file_content = self.download_file(file_id)
        if file_content:
            try:
                return pd.read_excel(io.BytesIO(file_content))
            except Exception as e:
                print(f"Error reading Excel: {e}")
                return None
        return None
    
    def get_file_by_name(self, filename: str) -> Optional[Dict[str, Any]]:
        """Get file metadata by filename."""
        files = self.list_files(f"name='{filename}'")
        return files[0] if files else None
    
    def get_recent_files(self, days: int = 7) -> List[Dict[str, Any]]:
        """Get files modified in the last N days."""
        from datetime import datetime, timedelta
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat() + 'Z'
        return self.list_files(f"modifiedTime > '{cutdown_date}'")

class GoogleDriveStream:
    """Stream data from Google Drive files."""
    
    def __init__(self, drive_connector: GoogleDriveConnector, file_id: str = None, filename: str = None, 
                 refresh_interval: int = 60):
        self.drive = drive_connector
        self.file_id = file_id
        self.filename = filename
        self.refresh_interval = refresh_interval
        self.last_modified = None
        
        if not file_id and filename:
            file_info = self.drive.get_file_by_name(filename)
            if file_info:
                self.file_id = file_info['id']
                self.last_modified = file_info['modifiedTime']
            else:
                raise ValueError(f"File '{filename}' not found in Google Drive")
    
    def get_data(self) -> Optional[pd.DataFrame]:
        """Get current data from the file."""
        if not self.file_id:
            return None
        
        # Check if file has been modified
        file_info = self.drive.service.files().get(fileId=self.file_id).execute()
        current_modified = file_info['modifiedTime']
        
        if self.last_modified != current_modified:
            self.last_modified = current_modified
            
            # Determine file type and read accordingly
            mime_type = file_info['mimeType']
            if 'csv' in mime_type:
                return self.drive.read_csv_from_drive(self.file_id)
            elif 'spreadsheet' in mime_type or 'excel' in mime_type:
                return self.drive.read_excel_from_drive(self.file_id)
        
        return None 