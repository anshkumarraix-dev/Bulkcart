import json
import os
from typing import Dict, Tuple
from google import genai
from google.genai import types
from models import ExtractionResponse, MerchantQuote

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

def get_cached_fallback(is_edited: bool = False) -> ExtractionResponse:
    fallback_file = os.path.join(DATA_DIR, "cached_fallback.json")
    with open(fallback_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    quotes = [MerchantQuote(**q) for q in data["quotes"]]
    return ExtractionResponse(
        quotes=quotes,
        counter_offer_draft=data["counter_offer_draft"]
    )

def extract_merchant_quotes(
    merchant_a: str,
    merchant_b: str,
    merchant_c: str,
    demand: Dict[str, int]
) -> Tuple[ExtractionResponse, bool, bool]:
    """
    Extracts structured quotes using Google Gemini with strict Pydantic JSON schema.
    Returns:
        (ExtractionResponse, used_fallback: bool, is_custom_edited: bool)
    """
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()
    timeout_sec = float(os.getenv("API_TIMEOUT_SECONDS", "10"))
    
    # Check if inputs match sample text
    households_file = os.path.join(DATA_DIR, "households.json")
    is_edited = False
    if os.path.exists(households_file):
        try:
            with open(households_file, "r", encoding="utf-8") as f:
                sample = json.load(f).get("sample_quotes", {})
            if (merchant_a.strip() != sample.get("merchant_a", "").strip() or
                merchant_b.strip() != sample.get("merchant_b", "").strip() or
                merchant_c.strip() != sample.get("merchant_c", "").strip()):
                is_edited = True
        except Exception:
            pass

    # If no API key configured or placeholder, immediately use cached fallback
    if not api_key or "your_" in api_key.lower():
        print("[LLM Extractor] No valid GEMINI_API_KEY found in .env; using cached fallback.")
        return get_cached_fallback(is_edited), True, is_edited

    prompt = f"""
You are the AI Buying Agent for a residential housing society (Gulmohar Enclave RWA).
The society is aggregating collective demand for this week's wholesale grocery round:
- Sona Masoori Rice: {demand.get('rice', 710)} kg
- Sharbati Atta: {demand.get('atta', 425)} kg
- Sunflower Oil: {demand.get('oil', 150)} L

Three local merchants have replied with messy, unstructured messages in broken English, raw price lists, and Hindi transcripts:

--- Merchant A Reply ---
{merchant_a}

--- Merchant B Reply ---
{merchant_b}

--- Merchant C Reply ---
{merchant_c}

Your task:
1. Extract the structured quote information for all three merchants into the requested JSON schema.
   - merchant_id must be "merchant_a", "merchant_b", or "merchant_c".
   - item_name must be normalized to lowercase: "rice", "atta", or "oil".
   - price_per_unit is numeric price per kg or L.
   - pack_sizes_offered: list of integer pack sizes mentioned (e.g. [25, 10] or [15]).
   - price_per_pack: list of corresponding float prices for each pack size.
   - Any unmentioned field must be null.
2. Generate a respectful, volume-leveraged counter-offer draft addressed to the best-priced merchant (written in courteous Hinglish/English like a society coordinator), citing the collective volume to request an extra 2% concession or free doorstep delivery.
"""

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ExtractionResponse,
                temperature=0.1
            )
        )
        
        parsed: ExtractionResponse = response.parsed
        if parsed and parsed.quotes:
            return parsed, False, is_edited
        else:
            print("[LLM Extractor] Gemini response parsing empty; falling back to cached.")
            return get_cached_fallback(is_edited), True, is_edited

    except Exception as e:
        print(f"[LLM Extractor] Gemini call failed ({type(e).__name__}: {e}); using cached fallback.")
        return get_cached_fallback(is_edited), True, is_edited
