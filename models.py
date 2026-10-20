from typing import List, Optional
from pydantic import BaseModel, Field

class QuoteItem(BaseModel):
    item_name: str = Field(description="Normalized commodity name: rice, atta, or oil")
    price_per_unit: float = Field(description="Price per kg or L")
    unit: str = Field(description="kg or L")
    pack_sizes_offered: List[int] = Field(default_factory=list, description="Available sack/tin sizes e.g. [25, 10]")
    price_per_pack: List[float] = Field(default_factory=list, description="Price per corresponding pack size")
    moq: Optional[int] = Field(default=None, description="Minimum order quantity in units, or null")

class MerchantQuote(BaseModel):
    merchant_id: str = Field(description="merchant_a, merchant_b, or merchant_c")
    merchant_name: str
    delivery_date: Optional[str] = None
    payment_terms: Optional[str] = None
    conditions: Optional[str] = None
    items: List[QuoteItem]

class ExtractionResponse(BaseModel):
    quotes: List[MerchantQuote]
    counter_offer_draft: str

class PackPlanItem(BaseModel):
    item_name: str
    demand_qty: int
    unit: str
    sacks_breakdown: str
    total_delivered_qty: int
    waste_qty: int

class MerchantAudit(BaseModel):
    merchant_id: str
    merchant_name: str
    total_cost: float
    badge_label: str
    badge_type: str
    is_best_pick: bool
    summary_notes: Optional[str] = None

class DemandItem(BaseModel):
    item_name: str
    quantity: int
    unit: str

class HouseholdOrder(BaseModel):
    flat_no: str
    resident_name: str
    rice_kg: int
    atta_kg: int
    oil_l: int

class SampleRoundResponse(BaseModel):
    society_name: str
    total_households: int
    demand: List[DemandItem]
    households: List[HouseholdOrder]
    sample_quotes: dict

class AnalyzeRequest(BaseModel):
    merchant_a_text: str
    merchant_b_text: str
    merchant_c_text: str

class VerdictResponse(BaseModel):
    best_merchant_id: str
    best_merchant_name: str
    total_retail_cost: float
    best_merchant_cost: float
    total_estimated_saving: float
    saving_percentage: float
    per_household_saving: float
    used_fallback: bool
    fallback_warning: Optional[str] = None
    pack_plans: List[PackPlanItem]
    merchant_audits: List[MerchantAudit]
    quotes: List[MerchantQuote]
    counter_offer_draft: str
