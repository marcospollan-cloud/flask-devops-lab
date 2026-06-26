# Flask DevOps Lab

## Usage

```
# Activate the virutal environment
source .venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Run the app
python app.py
```

## API Endpoints
* `/api/health`: monitors application status
* `/api/config`: displays configurations, including app name, version, and targets
* `/api/report`: displays system metrics, including host name, python version, and uptime
