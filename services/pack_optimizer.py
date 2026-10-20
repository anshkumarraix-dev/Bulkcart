import os
import sys
from typing import List, Tuple

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from models import PackPlanItem

def solve_pack_combination(demand: int, pack_sizes: List[int]) -> Tuple[List[Tuple[int, int]], int, int]:
    """
    Finds the optimal combination of standard pack sizes (e.g. [25, 10])
    that minimizes delivered excess (waste), prioritizing larger sacks to minimize bag count.
    
    Returns:
        (breakdown: [(count, pack_size), ...], total_delivered: int, waste: int)
    """
    if not pack_sizes:
        return ([(1, demand)], demand, 0)
    
    sorted_packs = sorted(pack_sizes, reverse=True)
    best_solution = None
    min_waste = float('inf')
    min_total_sacks = float('inf')
    
    largest = sorted_packs[0]
    max_largest = (demand // largest) + 2
    
    for count_largest in range(max_largest, -1, -1):
        delivered = count_largest * largest
        current_breakdown = [(count_largest, largest)] if count_largest > 0 else []
        
        remaining = max(0, demand - delivered)
        if len(sorted_packs) > 1:
            for p in sorted_packs[1:]:
                c = remaining // p
                if c > 0:
                    current_breakdown.append((c, p))
                    delivered += c * p
                    remaining -= c * p
            if remaining > 0:
                smallest = sorted_packs[-1]
                current_breakdown.append((1, smallest))
                delivered += smallest
        elif remaining > 0:
            current_breakdown.append((1, largest))
            delivered += largest
            
        waste = delivered - demand
        total_sacks = sum(c for c, _ in current_breakdown)
        
        if 0 <= waste < min_waste or (waste == min_waste and total_sacks < min_total_sacks):
            min_waste = waste
            min_total_sacks = total_sacks
            best_solution = (current_breakdown, delivered, waste)
            if waste == 0:
                break
                
    if best_solution is None:
        return ([(1, demand)], demand, 0)
    return best_solution


def optimize_demand_packs(demand_dict: dict, merchant_items: List) -> List[PackPlanItem]:
    """
    Takes demand amounts {"rice": 710, "atta": 425, "oil": 150} and extracted merchant items
    to generate zero-waste pack distribution plans.
    """
    plans = []
    
    default_packs = {
        "rice": [25, 10],
        "atta": [25, 10],
        "oil": [15]
    }
    
    units = {
        "rice": "kg",
        "atta": "kg",
        "oil": "L"
    }

    offered_packs = {}
    if merchant_items:
        for item in merchant_items:
            norm_name = getattr(item, "item_name", "") or ""
            normalized = norm_name.lower().strip()
            pack_sizes = getattr(item, "pack_sizes_offered", None)
            if pack_sizes:
                offered_packs[normalized] = pack_sizes
            
    for item_key, demand_val in demand_dict.items():
        packs = offered_packs.get(item_key, default_packs.get(item_key, [25]))
        unit_label = units.get(item_key, "units")
        container_word = "tins" if unit_label == "L" else "bags"
        
        breakdown, total_delivered, waste = solve_pack_combination(demand_val, packs)
        
        parts = [f"{count} × {size} {unit_label}" for count, size in breakdown if count > 0]
        breakdown_str = " + ".join(parts) + f" {container_word}" if parts else f"{demand_val} {unit_label}"
        
        plans.append(PackPlanItem(
            item_name=item_key,
            demand_qty=demand_val,
            unit=unit_label,
            sacks_breakdown=breakdown_str,
            total_delivered_qty=total_delivered,
            waste_qty=waste
        ))
        
    return plans
