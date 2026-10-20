---
doc: spec
status: approved
---

# Neighborhood Buying Agent — Technical Spec

## How This Works, In Plain Language

The app runs as a single local Python web server (FastAPI) that delivers a Retro Kirana-styled web page to your browser and handles the AI reasoning behind the scenes.

When the coordinator opens the app and clicks **"Load sample round"**, the browser pulls pre-seeded household data (26 homes needing 710 kg rice, 425 kg atta, and 150 L oil) and populates three editable text boxes with realistic, messy merchant quotes (broken English, a raw price list, and a transcribed Hindi voice note).

When the coordinator clicks **"Analyze quotes"**, the browser sends these raw texts to a FastAPI endpoint (`POST /api/analyze`). The backend forwards the text to Google Gemini via `google-genai` using a strict Pydantic JSON schema. Gemini does what AI is uniquely good at: reading unstructured human text and extracting structured pricing, units, bag sizes, and terms into clean JSON, while drafting a tailored counter-offer.

Immediately after extraction, the backend's deterministic Python engine takes over for the math:
1. It compares extracted unit prices to wholesale Mandi benchmarks to assign 3-state rubber-stamp badges:
   - **SAHI BHAV:** Within ±5% of mandi rate (Peacock Teal).
   - **MEHENGA (+X%):** More than 5% above mandi rate (Signboard Red).
   - **SAVDHAN (-X%):** More than 10% below mandi rate, or carrying a catch in conditions (Ochre Amber caution: "too good to be true, verify catch").
2. It runs a zero-waste bag combination solver across offered sack sizes (e.g. 28×25 kg + 1×10 kg bags for 710 kg rice, 17×25 kg for 425 kg atta, 10×15 L for 150 L oil).
3. It calculates total society savings against the realistic retail baseline (roughly ~₹10,000–₹14,000 on an ~₹80,000 retail baseline), displaying the exact computed figure dynamically as the headline.

The browser receives this clean JSON payload and renders the Quote Verdict. If the coordinator clicks **"Approve and send"**, the view transforms into a perforated **Pakka Bill** receipt slip ready for clipboard copying. 

If the Gemini API call ever times out (configurable `API_TIMEOUT_SECONDS = 10`) or encounters a rate limit:
- On unedited sample quotes: automatically displays the cached fallback with a discreet *"Using saved result (offline demo)"* tag.
- On user-edited quotes: displays the cached fallback with a clear disclaimer banner: *"API unavailable. Showing saved sample result (custom edits could not be analyzed)"*.

---

## The Core Journey Through the System

*Ref: [prd.md > The Core Journey](file:///c:/Users/Lenovo/OneDrive/Desktop/AI%20BASICS/devpost/prd.md#L14-L46)*

1. **Browser lands on `/`:** FastAPI serves `static/index.html`. `app.js` initializes the page in **State 1 (Empty)**: banner active, three quiet placeholder cards, "Analyze quotes" button disabled.
2. **Coordinator clicks "Load sample round":** `app.js` fetches `/api/sample-round`. It injects 26 households (710 kg rice, 425 kg atta, 150 L oil) into the Demand panel and populates the 3 merchant textareas. `app.js` transitions to **State 2 (Loaded)** and enables the "Analyze quotes" button.
3. **Coordinator clicks "Analyze quotes":** `app.js` switches UI to **State 3 (Analyzing)**, starts a simulated 4-step progress tick in the Verdict area, and sends a `POST /api/analyze` request with the merchant texts and demand quantities.
4. **Backend processes `/api/analyze`:**
   - Calls `services/llm_extractor.py` to prompt Gemini with `ExtractionResponse` Pydantic schema using model `GEMINI_MODEL` and timeout `API_TIMEOUT_SECONDS`.
   - If timeout or error occurs, loads `data/cached_fallback.json` and flags `used_fallback=True` (and checks whether inputs were modified).
   - Passes extracted data to `services/pack_optimizer.py` to calculate zero-waste sack distributions.
   - Passes data to `services/math_engine.py` to audit prices against `data/mandi_benchmark.json` and compute savings against `data/retail_baseline.json`.
   - Returns consolidated `VerdictResponse` JSON to browser.
5. **Browser displays Verdict:** `app.js` receives payload, stops progress checklist, and transitions to **State 4 (Verdict Rendered)**: headline savings banner (dynamically computed), side-by-side audit table with 3-state badges, pack-size breakdown card, and editable counter-offer box.
6. **Coordinator clicks "Approve and send":** `app.js` transitions to **State 6 (Pakka Bill Resolved)**: replaces the audit table with an animated perforated bill receipt with a red "SENT TO MERCHANT C (Simulated)" rubber stamp and clipboard copy button.
7. **Coordinator clicks "Start a new round":** Resets the DOM back to State 1.

---

## Stack

- **Backend Runtime:** Python 3.10+
- **Web Framework:** [FastAPI](https://fastapi.tiangolo.com/) (`fastapi>=0.110.0`)
  - *Rationale:* Single framework to serve the static frontend and REST endpoints in one process without CORS overhead.
- **ASGI Server:** [Uvicorn](https://www.uvicorn.org/) (`uvicorn[standard]>=0.28.0`)
  - *Rationale:* Lightweight, standard ASGI server for local development.
- **Data Validation & Schema:** [Pydantic v2](https://docs.pydantic.dev/latest/) (`pydantic>=2.6.0`)
  - *Rationale:* Native support for Gemini structured outputs via `response_schema`.
- **Environment Management:** [python-dotenv](https://github.com/theskumar/python-dotenv) (`python-dotenv>=1.0.0`)
  - *Rationale:* Keeps `GEMINI_API_KEY` and `GEMINI_MODEL` safely out of Git and client code.
- **LLM SDK:** [google-genai](https://github.com/googleapis/python-genai) (`google-genai>=0.1.0` or official SDK)
  - *Rationale:* Native structured JSON extraction on Gemini free tier (`gemini-2.5-flash` or `gemini-1.5-flash`).
- **Frontend:** Vanilla HTML5, CSS3, ES6 JavaScript (zero build tools, zero npm dependencies).
- **Fonts:** [Google Fonts](https://fonts.google.com/) (`Rozha One`, `Baloo 2`, `Noto Sans Devanagari`, `Space Mono`).

---

## Where It Runs and How Someone Tries It

- **Environment:** Local machine (Windows / macOS / Linux), Python 3.10+.
- **Setup:**
  ```bash
  pip install fastapi uvicorn pydantic python-dotenv google-genai
  # Copy .env.example to .env and configure:
  # GEMINI_API_KEY=your_key_here
  # GEMINI_MODEL=gemini-2.5-flash
  # API_TIMEOUT_SECONDS=10
  ```
- **Start Command:**
  ```bash
  uvicorn main:app --reload
  ```
- **What to Open:** Navigate to `http://127.0.0.1:8000` in Google Chrome or any modern browser.
- **Demo Recording:** Local screen recording (1 minute) walking through: Load sample round → Analyze quotes → Inspect Quote Verdict table and badges → Click Approve & Send to see the Pakka Bill.

---

## Look and Feel

*Ref: [prd.md > Look and Feel](file:///c:/Users/Lenovo/OneDrive/Desktop/AI%20BASICS/devpost/prd.md#L45-L72)*

- **CSS Implementation:** Pure Vanilla CSS in `static/style.css`.
- **Color Variables:**
  - `--bg-paper`: `#FDFBF7` (warm cream)
  - `--primary-marigold`: `#F5A623`
  - `--stamp-red`: `#D32F2F` (MEHENGA warning)
  - `--stamp-teal`: `#00897B` (SAHI BHAV success)
  - `--stamp-amber`: `#FF8F00` (SAVDHAN caution)
  - `--text-ink`: `#2C221E`
  - `--border-dark`: `#3E2723`
- **Visual Features:**
  - Pure CSS zigzag awning top banner using CSS `linear-gradient` clip-paths.
  - Perforated bill borders using CSS dashed/dotted pseudo-elements.
  - Bouncing CSS keyframe animations for rubber-stamp badges (`transform: rotate(-4deg) scale(...)`).

---

## Components

### 1. Frontend UI (`static/index.html`, `static/style.css`, `static/app.js`)
- Renders the main states (Empty, Loaded, Analyzing, Verdict, Pakka Bill).
- Coordinates the 4-step progress checklist during analysis.
- Handles user editing of quotes and displays *"Inputs changed, re-analyze"* notice.
- Ref: `prd.md > Screens and Layout`, `prd.md > States and Boundaries`.

### 2. FastAPI Application (`main.py`)
- Mounts `static/` directory to serve static assets and `index.html`.
- Exposes:
  - `GET /api/sample-round`: Returns seeded demand and sample merchant quote texts.
  - `POST /api/analyze`: Accepts quote texts and returns the complete parsed, audited, and optimized verdict.
  - `GET /api/health`: Healthcheck.

### 3. LLM Extraction Service (`services/llm_extractor.py`)
- Reads `GEMINI_MODEL` (default: `gemini-2.5-flash`) and `API_TIMEOUT_SECONDS` (default: `10`).
- Prompts Gemini with structured schema using Pydantic.
- Parses 3 merchant replies into typed data structures: unit price, pack sizes offered, MOQ, delivery date, terms, conditions.
- Drafts a volume-leveraged counter-offer string.
- Automatically catches timeouts/exceptions and falls back to `data/cached_fallback.json`.
- Ref: `prd.md > Features and Behavior > 2. Live Unstructured Quote Extraction`.

### 4. Deterministic Math & Audit Engine (`services/math_engine.py`)
- Audits extracted prices against `data/mandi_benchmark.json`:
  - `price <= mandi * 0.90` (or conditions mention delay/advance): **"SAVDHAN (-X%)"** (Peacock Amber caution: too cheap, check catch).
  - `mandi * 0.95 <= price <= mandi * 1.05`: **"SAHI BHAV"** (Peacock Teal fair price).
  - `price > mandi * 1.05`: **"MEHENGA (+X%)"** (Signboard Red overpriced).
- Evaluates total cost for each merchant based on consolidated demand (710 kg rice, 425 kg atta, 150 L oil).
- Selects "Best pick" merchant and calculates total savings dynamically against `data/retail_baseline.json` (~₹82,950 baseline yielding ~₹10,000–₹14,000 savings).
- Ref: `prd.md > Features and Behavior > 3. Seeded Baselines & Deterministic Math Engine`.

### 5. Pack-Size Optimizer (`services/pack_optimizer.py`)
- Exact sack solver: For each commodity demand (710 kg rice, 425 kg atta, 150 L oil), determines the optimal combination of standard pack sizes (25 kg, 10 kg, 15 L) resulting in zero product waste:
  - Rice: 28 × 25 kg + 1 × 10 kg = 710 kg (0 waste).
  - Atta: 17 × 25 kg = 425 kg (0 waste).
  - Oil: 10 × 15 L = 150 L (0 waste).
- Ref: `prd.md > Features and Behavior > 4. Zero-Waste Pack-Size Optimizer`.

---

## Data Model

### Pydantic Models (`models.py`)

```python
from typing import List, Optional
from pydantic import BaseModel, Field

class QuoteItem(BaseModel):
    item_name: str = Field(description="Normalized name: rice, atta, or oil")
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
    sacks_breakdown: str  # e.g. "28 × 25 kg + 1 × 10 kg"
    total_delivered_qty: int
    waste_qty: int  # 0

class MerchantAudit(BaseModel):
    merchant_id: str
    merchant_name: str
    total_cost: float
    badge_label: str  # "SAHI BHAV", "MEHENGA (+9%)", "SAVDHAN (-14%)"
    badge_type: str   # "fair", "expensive", "caution"
    is_best_pick: bool

class VerdictResponse(BaseModel):
    best_merchant_id: str
    best_merchant_name: str
    total_estimated_saving: float  # Computed dynamically
    saving_percentage: float       # Computed dynamically
    per_household_saving: float    # Computed dynamically
    used_fallback: bool
    fallback_warning: Optional[str] = None  # Populated if inputs were edited and fallback triggered
    pack_plans: List[PackPlanItem]
    merchant_audits: List[MerchantAudit]
    quotes: List[MerchantQuote]
    counter_offer_draft: str
```

---

## File Structure

```
c:\Users\Lenovo\OneDrive\Desktop\AI BASICS\
├── .env.example              # GEMINI_API_KEY, GEMINI_MODEL, API_TIMEOUT_SECONDS
├── .gitignore                # Ignores .env, __pycache__, /devpost/learner-profile.md
├── requirements.txt          # Python dependencies
├── main.py                   # FastAPI server entrypoint & API routes
├── models.py                 # Pydantic data schemas
├── services/
│   ├── __init__.py
│   ├── llm_extractor.py      # Google GenAI extraction & counter-offer prompt
│   ├── math_engine.py        # Mandi auditing (3-state badges) & retail savings
│   └── pack_optimizer.py     # Zero-waste bag combination solver
├── data/
│   ├── households.json       # 26 seeded households (710kg rice, 425kg atta, 150L oil)
│   ├── mandi_benchmark.json  # Wholesale Mandi reference rates
│   ├── retail_baseline.json  # Local retail prices (for savings baseline)
│   └── cached_fallback.json  # Guaranteed fallback payload for offline/timeout takes
├── static/
│   ├── index.html            # Single-screen dashboard structure
│   ├── style.css             # Retro Kirana styling, awning, stamps, pakka bill
│   └── app.js                # State management, progress timer, and API calls
└── devpost/                  # Hackathon planning workspace
    ├── learner-profile.md
    ├── scope.md
    ├── prd.md
    └── spec.md
```

---

## External Services and Dependencies

- **Service:** Google Gemini API
- **Model Config:** Configurable via `GEMINI_MODEL` (default: `gemini-2.5-flash` or `gemini-1.5-flash`)
- **Key Required:** `GEMINI_API_KEY` (Free tier from Google AI Studio)
- **Timeout:** Configurable via `API_TIMEOUT_SECONDS` (default: `10`)
- **Rate Limits:** 15 requests per minute (free tier). Handled cleanly via timeout + cached fallback.
- **Cost:** Free tier ($0.00).

---

## Important Failure Modes

1. **Gemini API Error or Timeout (>10s):**
   - *Sample Inputs:* Backend serves `data/cached_fallback.json` with a subtle tag: *"Using saved result (offline demo)"*.
   - *Edited Inputs:* Backend serves `data/cached_fallback.json` with a clear disclaimer banner: *"API unavailable. Showing saved sample result (custom edits could not be analyzed)"*.
2. **Missing Quote Fields in Raw Text:**
   - *Behavior:* Pydantic models assign `None` / `null` without throwing exceptions; UI renders `"—"` in comparison cells.
3. **Unexpected Text Editing after Analysis:**
   - *Behavior:* `app.js` listens to `input` events on quote textareas and renders a yellow *"Inputs changed, re-analyze"* notice, preventing automatic API quota drain.

---

## What Was Simplified and Why

- **FastAPI Static Mount** instead of separate React/Vite development server — eliminates CORS issues, Node.js build steps, and package-lock conflicts.
- **Seeded JSON files** instead of SQLite/PostgreSQL database — eliminates migrations, database setups, and connection strings while delivering the exact 26-home demand needed for the demo.
- **Clipboard Copy** instead of live WhatsApp Business API — avoids Meta developer account registration, webhook verification, and phone number provisioning.
- **Pre-transcribed Hindi text** instead of direct audio recording and Whisper API — avoids browser microphone permissions and audio upload complexity while proving the AI's multilingual comprehension.

---

## Decisions and Open Issues

- **Learner Decision 1 (Stack):** Selected Python FastAPI + Vanilla JS frontend for maximum control over math and zero bundler overhead.
- **Learner Decision 2 (LLM Provider & Config):** Selected Google Gemini free tier via `google-genai` with Pydantic structured output, with model name (`GEMINI_MODEL`) and timeout (`API_TIMEOUT_SECONDS`) externalized to `.env`.
- **Learner Decision 3 (Deterministic Logic & Realistic Baselines):** Restricted LLM to unstructured extraction and copy generation; all financial math, savings, 3-state badges, and pack optimization run deterministically in Python against realistic retail and mandi benchmarks.
- **Learner Uncertainty / Learning Focus:** Structured JSON extraction with Pydantic response schemas (Schema → Prompt → Parse).
  - *Clarification & Build Plan:* In `5-build`, we will write and test `services/pack_optimizer.py` first as a warm-up, and then build `services/llm_extractor.py` step-by-step so the learner sees how Pydantic models transform raw LLM text into verified, typed Python objects.

---

## Open Questions

*None. Technical blueprint is approved and ready for ordered build steps.*
