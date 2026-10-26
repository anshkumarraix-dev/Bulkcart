import json
import os
import sys

# Ensure project root is in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv

from models import (
    SampleRoundResponse, DemandItem, HouseholdOrder,
    AnalyzeRequest, VerdictResponse
)
from services.llm_extractor import extract_merchant_quotes
from services.math_engine import evaluate_merchant_quotes
from services.pack_optimizer import optimize_demand_packs

# Load environment variables
load_dotenv()

app = FastAPI(title="Bulkcart - AI Neighborhood Buying Agent API", version="1.0.0")

DATA_DIR = os.path.join(BASE_DIR, "data")
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Mount static folder
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
def serve_index():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

@app.get("/api/health")
def health_check():
    return {"status": "ok", "app": "Bulkcart - AI Neighborhood Buying Agent"}

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

@app.post("/api/analyze", response_model=VerdictResponse)
def analyze_quotes(req: AnalyzeRequest):
    # 1. Fetch current demand totals
    households_file = os.path.join(DATA_DIR, "households.json")
    demand = {"rice": 710, "atta": 425, "oil": 150}
    total_households = 26
    if os.path.exists(households_file):
        try:
            with open(households_file, "r", encoding="utf-8") as f:
                d = json.load(f)
                demand = d.get("demand_totals", demand)
                total_households = d.get("total_households", 26)
        except Exception:
            pass

    # 2. Extract quotes with Gemini (with cached fallback safety)
    extraction, used_fallback, is_edited = extract_merchant_quotes(
        merchant_a=req.merchant_a_text,
        merchant_b=req.merchant_b_text,
        merchant_c=req.merchant_c_text,
        demand=demand
    )

    fallback_warning = None
    if used_fallback and is_edited:
        fallback_warning = "API unavailable or rate-limited. Showing saved sample result (custom edits could not be analyzed)."

    # 3. Deterministic math engine evaluates Mandi badges & savings vs retail
    (
        audits, best_id, best_name,
        retail_cost, best_cost, saving, saving_pct, per_home
    ) = evaluate_merchant_quotes(
        quotes=extraction.quotes,
        demand=demand,
        total_households=total_households
    )

    # 4. Pack optimizer calculates zero-waste sack breakdowns
    best_quote = next((q for q in extraction.quotes if q.merchant_id == best_id), extraction.quotes[0] if extraction.quotes else None)
    best_items = best_quote.items if best_quote else []
    pack_plans = optimize_demand_packs(demand, best_items)

    return VerdictResponse(
        best_merchant_id=best_id,
        best_merchant_name=best_name,
        total_retail_cost=retail_cost,
        best_merchant_cost=best_cost,
        total_estimated_saving=saving,
        saving_percentage=saving_pct,
        per_household_saving=per_home,
        used_fallback=used_fallback,
        fallback_warning=fallback_warning,
        pack_plans=pack_plans,
        merchant_audits=audits,
        quotes=extraction.quotes,
        counter_offer_draft=extraction.counter_offer_draft
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


