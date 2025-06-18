from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
from typing import Dict, Any
import pathway as pw
from microhack.pipeline import pipeline
from microhack.input import input
from microhack.output import output
from microhack.config import get_settings

app = FastAPI(title="MicroHack API", description="Pathway-based data processing API")

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state for current sum
current_sum = 0

@app.get("/")
async def root():
    return {"message": "MicroHack API is running"}

@app.get("/health")
async def health():
    return {"status": "healthy", "current_sum": current_sum}

@app.post("/process-data")
async def process_data(data: Dict[str, Any]):
    """Process a single data point"""
    global current_sum
    value = data.get("value", 0)
    current_sum += value
    return {"processed_value": value, "current_sum": current_sum}

@app.websocket("/ws/stream")
async def websocket_stream(websocket: WebSocket):
    """WebSocket endpoint for real-time data streaming"""
    await websocket.accept()
    
    try:
        # Initialize Pathway pipeline
        get_settings()
        input_table = input()
        output_table = pipeline(input_table)
        
        # Create a custom output that sends data to WebSocket
        def websocket_output(table):
            def callback(key, row, time, is_addition):
                asyncio.create_task(
                    websocket.send_text(
                        json.dumps({
                            "key": key,
                            "sum": row["sum"],
                            "timestamp": time,
                            "is_addition": is_addition
                        })
                    )
                )
            
            table.subscribe(callback)
        
        websocket_output(output_table)
        
        # Keep connection alive
        while True:
            await asyncio.sleep(1)
            await websocket.ping()
            
    except Exception as e:
        await websocket.close(code=1000, reason=str(e))

@app.get("/stats")
async def get_stats():
    """Get current processing statistics"""
    return {
        "current_sum": current_sum,
        "status": "running"
    } 