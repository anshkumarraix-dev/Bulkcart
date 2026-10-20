import json
import os
import sys

# Add root directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from fastapi.testclient import TestClient
from main import app

def test_api_analyze():
    print("--- Testing POST /api/analyze Endpoint ---")
    client = TestClient(app)
    
    with open("data/households.json", "r", encoding="utf-8") as f:
        sample_quotes = json.load(f)["sample_quotes"]
        
    payload = {
        "merchant_a_text": sample_quotes["merchant_a"],
        "merchant_b_text": sample_quotes["merchant_b"],
        "merchant_c_text": sample_quotes["merchant_c"]
    }
    
    res = client.post("/api/analyze", json=payload)
    print("Response Status Code:", res.status_code)
    assert res.status_code == 200, f"Expected 200, got {res.status_code}: {res.text}"
    
    data = res.json()
    print("Best Merchant Selected:", data["best_merchant_name"], f"({data['best_merchant_id']})")
    print(f"Total Retail Cost: ₹{data['total_retail_cost']}")
    print(f"Best Merchant Cost: ₹{data['best_merchant_cost']}")
    print(f"Calculated Saving: ₹{data['total_estimated_saving']} ({data['saving_percentage']}%)")
    print(f"Per Household Saving: ₹{data['per_household_saving']}")
    print(f"Used Fallback: {data['used_fallback']}")
    
    assert data["best_merchant_id"] in ["merchant_a", "merchant_b", "merchant_c"]
    assert len(data["pack_plans"]) == 3, "Expected 3 pack plans (rice, atta, oil)"
    for p in data["pack_plans"]:
        print(f"  - {p['item_name'].title()}: {p['sacks_breakdown']} (Waste: {p['waste_qty']} kg)")
        assert p["waste_qty"] == 0, "Pack plan must have zero waste"
        
    assert len(data["merchant_audits"]) == 3, "Expected 3 merchant audits"
    for a in data["merchant_audits"]:
        print(f"  - {a['merchant_name']}: {a['badge_label']}")
        
    assert len(data["counter_offer_draft"].strip()) > 10, "Counter offer draft must be populated"
    print("\nCounter Offer Draft Preview:\n", data["counter_offer_draft"][:160], "...\n")
    
    # Test edited text scenario
    payload_edited = {
        "merchant_a_text": "Custom edited price: rice 80 rs",
        "merchant_b_text": "Custom edited price: rice 75 rs",
        "merchant_c_text": "Custom edited price: rice 70 rs"
    }
    res_edited = client.post("/api/analyze", json=payload_edited)
    assert res_edited.status_code == 200
    data_edited = res_edited.json()
    print("Edited Input Test - Used Fallback:", data_edited["used_fallback"])
    if data_edited["used_fallback"]:
        print("Fallback Warning:", data_edited["fallback_warning"])
        assert data_edited["fallback_warning"] is not None
        
    print(">> All Slice 2 Verification Tests Passed Successfully!")

if __name__ == "__main__":
    test_api_analyze()
