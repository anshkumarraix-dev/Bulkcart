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

from services.pack_optimizer import solve_pack_combination, optimize_demand_packs
from services.math_engine import evaluate_merchant_quotes
from models import MerchantQuote

def test_pack_optimizer():
    print("--- 1. Testing Zero-Waste Pack Optimizer ---")
    
    # Test Rice (710 kg)
    breakdown, total, waste = solve_pack_combination(710, [25, 10])
    print(f"Rice (710 kg): {breakdown} -> Total: {total} kg, Waste: {waste} kg")
    assert total == 710, f"Expected 710, got {total}"
    assert waste == 0, f"Expected 0 waste, got {waste}"
    assert (28, 25) in breakdown and (1, 10) in breakdown
    
    # Test Atta (425 kg)
    breakdown, total, waste = solve_pack_combination(425, [25, 10])
    print(f"Atta (425 kg): {breakdown} -> Total: {total} kg, Waste: {waste} kg")
    assert total == 425, f"Expected 425, got {total}"
    assert waste == 0, f"Expected 0 waste, got {waste}"
    assert (17, 25) in breakdown
    
    # Test Oil (150 L)
    breakdown, total, waste = solve_pack_combination(150, [15])
    print(f"Oil (150 L): {breakdown} -> Total: {total} L, Waste: {waste} L")
    assert total == 150, f"Expected 150, got {total}"
    assert waste == 0, f"Expected 0 waste, got {waste}"
    assert (10, 15) in breakdown
    
    print(">> Pack Optimizer Passed Perfectly! Zero Waste Verified.\n")

def test_math_engine():
    print("--- 2. Testing Math Engine & Mandi Audit ---")
    with open("data/cached_fallback.json", "r", encoding="utf-8") as f:
        fallback = json.load(f)
        
    quotes = [MerchantQuote(**q) for q in fallback["quotes"]]
    demand = {"rice": 710, "atta": 425, "oil": 150}
    
    audits, best_id, best_name, retail_cost, best_cost, saving, saving_pct, per_home = evaluate_merchant_quotes(
        quotes=quotes,
        demand=demand,
        total_households=26
    )
    
    print(f"Total Retail Cost: ₹{retail_cost}")
    print(f"Best Merchant: {best_name} (ID: {best_id}) with Cost: ₹{best_cost}")
    print(f"Total Savings: ₹{saving} ({saving_pct}%)")
    print(f"Per Household Saving: ₹{per_home}")
    
    for a in audits:
        print(f"  - {a.merchant_name}: {a.badge_label} (Total: ₹{a.total_cost})")
        
    assert best_id == "merchant_c", f"Expected merchant_c as best, got {best_id}"
    assert saving > 10000, f"Expected savings > 10,000, got {saving}"
    assert retail_cost > best_cost, "Retail must be greater than best wholesale cost"
    
    badges = {a.merchant_id: a.badge_label for a in audits}
    assert "MEHENGA" in badges["merchant_a"]
    assert "MEHENGA" in badges["merchant_b"]
    assert "SAHI BHAV" in badges["merchant_c"]
    
    print(">> Math Engine Passed Perfectly! Realistic Baselines & Badges Verified.\n")

if __name__ == "__main__":
    test_pack_optimizer()
    test_math_engine()
    print("ALL SLICE 1 UNIT TESTS PASSED!")
