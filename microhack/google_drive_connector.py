import time
import pandas as pd
from typing import Dict, Any, Optional
import pathway as pw
from microhack.google_drive import GoogleDriveConnector, GoogleDriveStream
import os

class GoogleDrivePathwayConnector(pw.io.python.ConnectorSubject):
    """Pathway connector for Google Drive data streaming."""
    
    def __init__(self, 
                 credentials_file: str = "config/credentials.json",
                 file_id: str = None,
                 filename: str = None,
                 refresh_interval: int = 60,
                 value_column: str = "value"):
        super().__init__()
        
        # Check if token exists first
        token_file = "config/token.json"
        if not os.path.exists(token_file):
            raise FileNotFoundError(
                f"Authentication token not found: {token_file}\n"
                "Please run './setup_auth.py' first to authenticate with Google Drive."
            )
        
        try:
            self.drive_connector = GoogleDriveConnector(credentials_file)
        except Exception as e:
            print(f"Error initializing Google Drive connector: {e}")
            print("Please ensure you have:")
            print("1. credentials.json in config/ directory")
            print("2. Run './setup_auth.py' to authenticate")
            raise
        
        self.file_id = file_id
        self.filename = filename
        self.refresh_interval = refresh_interval
        self.value_column = value_column
        self.last_data = None
        
        # Initialize the stream
        if not file_id and filename:
            file_info = self.drive_connector.get_file_by_name(filename)
            if file_info:
                self.file_id = file_info['id']
            else:
                raise ValueError(f"File '{filename}' not found in Google Drive")
    
    def run(self):
        """Main loop that streams data from Google Drive."""
        print(f"Starting Google Drive stream for file: {self.filename or self.file_id}")
        
        while True:
            try:
                # Get current data from Google Drive
                if self.file_id:
                    file_info = self.drive_connector.service.files().get(fileId=self.file_id).execute()
                    mime_type = file_info['mimeType']
                    
                    # Read data based on file type
                    if 'csv' in mime_type:
                        df = self.drive_connector.read_csv_from_drive(self.file_id)
                    elif 'spreadsheet' in mime_type or 'excel' in mime_type:
                        df = self.drive_connector.read_excel_from_drive(self.file_id)
                    else:
                        print(f"Unsupported file type: {mime_type}")
                        time.sleep(self.refresh_interval)
                        continue
                    
                    if df is not None and not df.empty:
                        # Check if data has changed
                        if self.last_data is None or not df.equals(self.last_data):
                            self.last_data = df.copy()
                            
                            # Stream each row as a separate event
                            for index, row in df.iterrows():
                                # Convert row to dictionary
                                row_dict = row.to_dict()
                                
                                # Ensure we have a 'value' field for the pipeline
                                if self.value_column in row_dict:
                                    value = row_dict[self.value_column]
                                else:
                                    # If no value column, use the first numeric column or default to 1
                                    numeric_cols = df.select_dtypes(include=['number']).columns
                                    if len(numeric_cols) > 0:
                                        value = row_dict[numeric_cols[0]]
                                    else:
                                        value = 1
                                
                                # Create event data
                                event_data = {
                                    "value": float(value),
                                    "row_index": int(index),
                                    "timestamp": time.time(),
                                    **row_dict  # Include all original columns
                                }
                                
                                # Send to Pathway
                                self.next_json(event_data)
                                
                                # Small delay between rows to avoid overwhelming the pipeline
                                time.sleep(0.1)
                            
                            print(f"Streamed {len(df)} rows from Google Drive")
                
                # Wait before next check
                time.sleep(self.refresh_interval)
                
            except Exception as e:
                print(f"Error in Google Drive stream: {e}")
                time.sleep(self.refresh_interval)

def google_drive_input(file_id: str = None, 
                      filename: str = None,
                      credentials_file: str = "config/credentials.json",
                      refresh_interval: int = 60,
                      value_column: str = "value"):
    """Create a Pathway input from Google Drive."""
    
    class GoogleDriveSchema(pw.Schema):
        value: float
        row_index: int
        timestamp: float
        # Additional fields will be added dynamically
    
    connector = GoogleDrivePathwayConnector(
        credentials_file=credentials_file,
        file_id=file_id,
        filename=filename,
        refresh_interval=refresh_interval,
        value_column=value_column
    )
    
    return pw.io.python.read(
        connector,
        schema=GoogleDriveSchema,
        format="json",
        autocommit_duration_ms=1000
    ) 