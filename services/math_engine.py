import json
import os
import sys
from typing import List, Dict, Tuple

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from models import MerchantQuote, MerchantAudit

DATA_DIR = os.path.join(PROJECT_ROOT, "data")

def load_benchmarks() -> Tuple[dict, dict]:
    with open(os.path.join(DATA_DIR, "mandi_benchmark.json"), "r", encoding="utf-8") as f:
        mandi = json.load(f)["rates"]
    with open(os.path.join(DATA_DIR, "retail_baseline.json"), "r", encoding="utf-8") as f:
        retail = json.load(f)["rates"]
    return mandi, retail

def evaluate_merchant_quotes(
    quotes: List[MerchantQuote],
    demand: Dict[str, int],
    total_households: int = 26
) -> Tuple[List[MerchantAudit], str, str, float, float, float, float, float]:
    """
    Evaluates quotes deterministically against retail baseline and Mandi benchmark.
    Returns:
        (merchant_audits, best_merchant_id, best_merchant_name,
         total_retail_cost, best_merchant_cost, total_saving, saving_pct, per_household_saving)
    """
    mandi_rates, retail_rates = load_benchmarks()
    
    # 1. Compute total retail baseline cost
    total_retail_cost = 0.0
    for item_name, qty in demand.items():
        unit_retail = retail_rates.get(item_name, {}).get("price_per_unit", 0.0)
        total_retail_cost += qty * unit_retail
        
    audits = []
    best_merchant_id = ""
    best_merchant_name = ""
    min_cost = float("inf")
    
    for q in quotes:
        merchant_cost = 0.0
        mandi_pct_diffs = []
        
        # Calculate cost & Mandi comparison for each quoted item
        for item in q.items:
            norm_name = item.item_name.lower().strip()
            qty = demand.get(norm_name, 0)
            merchant_cost += qty * item.price_per_unit
            
            mandi_benchmark = mandi_rates.get(norm_name, {}).get("price_per_unit")
            if mandi_benchmark and mandi_benchmark > 0:
                diff_pct = ((item.price_per_unit - mandi_benchmark) / mandi_benchmark) * 100.0
                mandi_pct_diffs.append(diff_pct)
                
        # Average deviation vs Mandi
        avg_diff = sum(mandi_pct_diffs) / len(mandi_pct_diffs) if mandi_pct_diffs else 0.0
        
        # Determine 3-state badge rules:
        # - SAHI BHAV: within +-5% of mandi rate
        # - MEHENGA (+X%): more than 5% above mandi rate
        # - SAVDHAN (-X%): more than 10% below mandi rate, or catch in conditions
        conditions_lower = (q.conditions or "").lower()
        has_catch = any(w in conditions_lower for w in ["advance", "damaged", "old stock", "non-refundable"])
        
        if avg_diff < -10.0 or has_catch:
            badge_label = f"SAVDHAN ({int(avg_diff)}%)" if avg_diff < 0 else "SAVDHAN"
            badge_type = "caution"
            summary_notes = "Rate is suspiciously low or has restrictive payment terms. Check quality."
        elif avg_diff > 5.0:
            badge_label = f"MEHENGA (+{int(round(avg_diff))}%)"
            badge_type = "expensive"
            summary_notes = f"Prices are {int(round(avg_diff))}% above wholesale mandi benchmark."
        else:
            badge_label = "SAHI BHAV"
            badge_type = "fair"
            summary_notes = "Fair wholesale rate matching APMC Mandi standards."
            
        audits.append({
            "merchant_id": q.merchant_id,
            "merchant_name": q.merchant_name,
            "total_cost": round(merchant_cost, 2),
            "badge_label": badge_label,
            "badge_type": badge_type,
            "summary_notes": summary_notes,
            "avg_diff": avg_diff
        })
        
        if merchant_cost < min_cost:
            min_cost = merchant_cost
            best_merchant_id = q.merchant_id
            best_merchant_name = q.merchant_name

    # Create final typed MerchantAudit list
    final_audits = []
    for a in audits:
        final_audits.append(MerchantAudit(
            merchant_id=a["merchant_id"],
            merchant_name=a["merchant_name"],
            total_cost=a["total_cost"],
            badge_label=a["badge_label"],
            badge_type=a["badge_type"],
            is_best_pick=(a["merchant_id"] == best_merchant_id),
            summary_notes=a["summary_notes"]
        ))
        
    best_merchant_cost = min_cost if min_cost != float("inf") else total_retail_cost
    total_saving = max(0.0, total_retail_cost - best_merchant_cost)
    saving_pct = (total_saving / total_retail_cost) * 100.0 if total_retail_cost > 0 else 0.0
    per_household = total_saving / total_households if total_households > 0 else 0.0
    
    return (
        final_audits,
        best_merchant_id,
        best_merchant_name,
        round(total_retail_cost, 2),
        round(best_merchant_cost, 2),
        round(total_saving, 2),
        round(saving_pct, 1),
        round(per_household, 2)
    )
