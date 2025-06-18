# MicroHack - Real-time Data Processing Pipeline

A Pathway-based real-time data processing microservice with API integration, frontend dashboard, and Google Drive integration.

## 🏗️ Project Architecture

```
Frontend (HTML/JS) ←→ API Server (FastAPI) ←→ Pathway Pipeline ←→ Data Sources (Google Drive/Kafka/Python)
```

### Core Components:
- **`pipeline.py`**: Business logic (currently sums all input values)
- **`input.py`**: Data ingestion (Python stream, Kafka, or Google Drive)
- **`output.py`**: Data output (CSV file or WebSocket)
- **`api.py`**: REST API and WebSocket server
- **`config.py`**: Configuration management
- **`google_drive.py`**: Google Drive API integration
- **`google_drive_connector.py`**: Pathway-compatible Google Drive connector

## 🚀 Quick Start

### 1. Build and Test
```bash
# Build containers
docker compose -f local.yml build

# Run unit tests
docker compose -f local.yml run --rm pathway_app pytest

# Run streaming mode (real-time data processing)
docker compose -f local.yml up
```

### 2. API Server with Frontend
```bash
# Build API server
docker compose -f api.yml build

# Start API server
docker compose -f api.yml up

# Open frontend-example.html in your browser
# Or visit http://localhost:8000 for API documentation
```

### 3. Google Drive Integration
```bash
# Step 1: Run setup script (choose one):
./setup.sh                    # Shell script (recommended)
./setup_google_drive.py       # Direct Python script
python3 setup_google_drive.py # Explicit python3 command

# Step 2: Set up Google Cloud credentials (follow setup instructions)
# - Create Google Cloud project
# - Enable Google Drive API
# - Download credentials.json to config/ directory

# Step 3: Authenticate with Google Drive (outside Docker):
./setup_auth.py               # This handles OAuth authentication

# Step 4: Upload sample data to Google Drive:
./upload_to_drive.py          # Uploads sample_data.csv to Google Drive

# Step 5: Build and run Google Drive containers:
docker compose -f google_drive.yml build
docker compose -f google_drive.yml up
```

### 4. Production Mode (Kafka)
```bash
# Clean previous state
docker compose -f prod.yml rm -svf

# Start production environment
docker compose -f prod.yml up

# Test with Kafka messages
docker compose -f prod.yml exec kafka kafka-console-producer \
  --bootstrap-server kafka:9092 --topic stock-data
# Then type: {"value":10}
```

## 🔗 Google Drive Integration

### Setup Instructions

#### 1. Google Cloud Console Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the Google Drive API:
   - Go to 'APIs & Services' > 'Library'
   - Search for 'Google Drive API'
   - Click 'Enable'
4. Create credentials:
   - Go to 'APIs & Services' > 'Credentials'
   - Click 'Create Credentials' > 'OAuth 2.0 Client IDs'
   - Choose 'Desktop application'
   - Download the JSON file
5. Rename the downloaded file to `credentials.json`
6. Place it in the `config/` directory

#### 2. Sample Data Setup
1. Upload `sample_data.csv` to your Google Drive
2. Note the filename (default: 'sample_data.csv')
3. Make sure the file is accessible to your Google account

#### 3. Configuration
Create `config/.env` file:
```env
INPUT_CONNECTOR=google_drive
GOOGLE_DRIVE_FILENAME=sample_data.csv
GOOGLE_DRIVE_REFRESH_INTERVAL=30
GOOGLE_DRIVE_VALUE_COLUMN=value
```

#### 4. Testing
```bash
# Build and run
docker compose -f google_drive.yml build
docker compose -f google_drive.yml up
```

The application will:
- Authenticate with Google Drive (browser will open)
- Find and read your CSV file
- Stream data through the Pathway pipeline
- Output results to `output.csv`

### Supported File Types
- **CSV files**: Automatically detected and parsed
- **Excel files**: Both .xlsx and .xls formats
- **Google Sheets**: Accessible via Google Drive API

### Data Format
Your Google Drive file should have a column that can be used as the "value" for processing. The default column name is "value", but you can configure it via `GOOGLE_DRIVE_VALUE_COLUMN`.

Example CSV structure:
```csv
value,timestamp,category,description
10,2024-01-01 10:00:00,A,First entry
25,2024-01-01 10:01:00,B,Second entry
15,2024-01-01 10:02:00,A,Third entry
```

## 🧪 Testing & Visual Feedback

### Unit Testing
```bash
docker compose -f local.yml run --rm pathway_app pytest
```
- Tests pipeline logic with sample data
- Verifies sum operation works correctly

### Streaming Mode (Real-time)
```bash
docker compose -f local.yml up
```
- Generates continuous data every 100ms
- Outputs real-time results to `output.csv`
- Format: `sum,timestamp,operation`

### Google Drive Mode
```bash
docker compose -f google_drive.yml up
```
- Reads data from Google Drive file
- Monitors for file changes
- Streams updates through pipeline
- Refresh interval configurable (default: 30 seconds)

### API Testing
```bash
# Health check
curl http://localhost:8000/health

# Process data
curl -X POST http://localhost:8000/process-data \
  -H "Content-Type: application/json" \
  -d '{"value": 5}'

# Get statistics
curl http://localhost:8000/stats
```

## 🔗 Frontend Integration

### Option 1: HTML Dashboard
Open `frontend-example.html` in your browser to see:
- Real-time statistics dashboard
- WebSocket connection for live updates
- Manual data input controls
- Activity log

### Option 2: Custom Frontend
Connect to the API endpoints:

**REST API:**
- `GET /health` - Service health and current sum
- `POST /process-data` - Process single data point
- `GET /stats` - Current processing statistics

**WebSocket:**
- `ws://localhost:8000/ws/stream` - Real-time data streaming

### Option 3: React/Vue/Angular Integration
```javascript
// Example React hook for WebSocket
const useWebSocket = () => {
  const [data, setData] = useState(null);
  
  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws/stream');
    ws.onmessage = (event) => {
      setData(JSON.parse(event.data));
    };
    return () => ws.close();
  }, []);
  
  return data;
};
```

## 🔧 Configuration

### Environment Variables
Create `config/.env` file:
```env
# Input connector type
INPUT_CONNECTOR=python  # or kafka or google_drive
PATHWAY_THREADS=1
AUTOCOMMIT_DURATION_MS=1000

# Kafka settings (for production)
KAFKA_BOOTSTRAP_SERVERS=kafka:9092
KAFKA_GROUP_ID=my-group
KAFKA_SESSION_TIMEOUT_MS=6000
KAFKA_TOPIC=stock-data

# Google Drive settings
GOOGLE_DRIVE_FILENAME=sample_data.csv
GOOGLE_DRIVE_REFRESH_INTERVAL=30
GOOGLE_DRIVE_VALUE_COLUMN=value
```

### Customizing the Pipeline
Edit `microhack/pipeline.py` to implement your business logic:

```python
def pipeline(input_table: pw.Table) -> pw.Table:
    """Your custom logic."""
    
    # Example: Calculate moving average
    output_table = input_table.windowby(
        pw.this.timestamp,
        window=pw.window.sliding(duration=timedelta(seconds=10))
    ).reduce(
        avg_value=pw.reducers.avg(pw.this.value)
    )
    
    return output_table
```

## 📊 Data Flow

### Current Pipeline
1. **Input**: Data from Python stream, Kafka, or Google Drive
2. **Processing**: Pathway sums all incoming values in real-time
3. **Output**: Results written to `output.csv` or sent via WebSocket

### Google Drive Flow
1. **Authentication**: OAuth 2.0 with Google Drive API
2. **File Monitoring**: Checks for file changes every 30 seconds
3. **Data Reading**: Downloads and parses CSV/Excel files
4. **Streaming**: Sends each row as a separate event to Pathway
5. **Processing**: Real-time aggregation and analysis

### Custom Data Sources
Modify `microhack/input.py` to connect to:
- Databases (PostgreSQL, MySQL)
- Message queues (RabbitMQ, Redis)
- File systems
- External APIs
- Google Drive (already implemented)

### Custom Outputs
Modify `microhack/output.py` to send data to:
- Databases
- Message queues
- HTTP endpoints
- WebSocket clients

## 🐳 Docker Services

### Development (`local.yml`)
- Single container with Python stream input
- Volume mounting for live code changes
- Debug-friendly configuration

### API Server (`api.yml`)
- FastAPI server with WebSocket support
- CORS enabled for frontend integration
- Port 8000 exposed

### Google Drive (`google_drive.yml`)
- Google Drive API integration
- File monitoring and streaming
- OAuth 2.0 authentication

### Production (`prod.yml`)
- Kafka for scalable data ingestion
- Multiple Pathway threads
- Production-optimized settings

## 🔍 Monitoring & Debugging

### Pathway Monitoring
The application runs with full monitoring enabled:
```python
pw.run(monitoring_level=pw.MonitoringLevel.ALL)
```

### API Documentation
Visit `http://localhost:8000/docs` for interactive API documentation.

### Logs
```bash
# View application logs
docker compose -f local.yml logs pathway_app

# View API server logs
docker compose -f api.yml logs api_server

# View Google Drive logs
docker compose -f google_drive.yml logs pathway_app
```

## 🛠️ Troubleshooting

### Google Drive Authentication Issues

**Error: "could not locate runnable browser"**
- This happens when running OAuth in Docker containers
- **Solution**: Run authentication outside Docker first:
  ```bash
  ./setup_auth.py  # Run this on your host machine
  ```

**Error: "Authentication token not found"**
- The OAuth token hasn't been created yet
- **Solution**: Run the authentication setup:
  ```bash
  ./setup_auth.py
  ```

**Error: "Credentials file not found"**
- The `credentials.json` file is missing
- **Solution**: Download from Google Cloud Console and place in `config/` directory

**Error: "File not found in Google Drive"**
- The specified file doesn't exist in your Google Drive
- **Solution**: Upload the file first:
  ```bash
  ./upload_to_drive.py
  ```

### General Issues

**Docker build fails**
- Check that all requirements are installed
- Try rebuilding: `docker compose -f google_drive.yml build --no-cache`

**Permission denied errors**
- Make sure files are executable: `chmod +x *.py *.sh`

**Port conflicts**
- Change ports in the Docker Compose files if needed
- Check if port 8000 is already in use

## 🚀 Deployment

### Local Development
1. Use `local.yml` for development
2. Use `api.yml` for frontend integration
3. Use `google_drive.yml` for Google Drive testing
4. Use `prod.yml` for production-like testing

### Production Deployment
1. Configure environment variables
2. Set up Google Drive credentials securely
3. Set up Kafka cluster (if using)
4. Deploy with production Docker Compose
5. Set up monitoring and logging

## 📝 Next Steps

1. **Customize Pipeline**: Implement your specific business logic
2. **Add Data Sources**: Connect to your data streams
3. **Enhance Frontend**: Build a production-ready dashboard
4. **Add Authentication**: Secure the API endpoints
5. **Scale**: Deploy to Kubernetes or cloud platforms
6. **Google Drive Features**: Add support for multiple files, folders, etc.

## 🛠️ Dependencies

- **Pathway**: Real-time data processing engine
- **FastAPI**: Modern web framework for APIs
- **Docker**: Containerization
- **Kafka**: Message streaming (production)
- **Google Drive API**: File access and streaming
- **Pandas**: Data manipulation
- **Pydantic**: Data validation and settings
