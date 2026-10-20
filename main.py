import json
import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv

from models import SampleRoundResponse, DemandItem, HouseholdOrder

# Load environment variables
load_dotenv()

app = FastAPI(title="Neighborhood Buying Agent API", version="1.0.0")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Mount static folder
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
def serve_index():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

@app.get("/api/health")
def health_check():
    return {"status": "ok", "app": "Neighborhood Buying Agent"}

@app.get("/api/sample-round", response_model=SampleRoundResponse)
def get_sample_round():
    households_file = os.path.join(DATA_DIR, "households.json")
    if not os.path.exists(households_file):
        raise HTTPException(status_code=404, detail="Sample households data not found")
        
    with open(households_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    demand_items = [
        DemandItem(item_name="rice", quantity=data["demand_totals"]["rice"], unit="kg"),
        DemandItem(item_name="atta", quantity=data["demand_totals"]["atta"], unit="kg"),
        DemandItem(item_name="oil", quantity=data["demand_totals"]["oil"], unit="L")
    ]
    
    households = [HouseholdOrder(**h) for h in data["households"]]
    
    return SampleRoundResponse(
        society_name=data["society_name"],
        total_households=data["total_households"],
        demand=demand_items,
        households=households,
        sample_quotes=data["sample_quotes"]
    )
