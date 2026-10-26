# 🛒 Bulkcart — AI Neighborhood Buying Agent

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![Google Gemini](https://img.shields.io/badge/Google%20GenAI-Gemini%202.5%20Flash-orange.svg)](https://ai.google.dev/)
[![Devpost Hackathon](https://img.shields.io/badge/Devpost-Build%20With%20AI%20Basics-blueviolet.svg)](https://learn-ai-basics.devpost.com/)
[![Tests](https://img.shields.io/badge/Tests-Passing%20(100%25)-success.svg)](tests/)

> **"Societies buy like wholesalers • Save visibly every single week."**  
> Bulkcart is an AI-powered buying agent for residential societies and neighborhood RWAs. It aggregates household demand for staple groceries, parses chaotic multilingual merchant quotes via Google Gemini structured schemas, audits prices against wholesale Mandi benchmarks, solves zero-waste commercial sack combinations, and issues an animated **Pakka Bill** resolution receipt with ready-to-dispatch counter-offers.

---

## 📑 Table of Contents

- [The Problem & Impact](#-the-problem--real-world-impact)
- [How Bulkcart Works](#-how-bulkcart-works)
- [60-Second Interactive Demo Guide](#-60-second-interactive-demo-guide)
- [System Architecture](#-system-architecture)
- [Tech Stack](#-tech-stack)
- [Quick Start & Local Setup](#-quick-start--local-setup)
- [Testing & Verification](#-testing--verification)
- [Devpost Learn Skill Pack Artifacts](#-devpost-learn-skill-pack-artifacts)
- [Repository Structure](#-repository-structure)
- [License](#-license)

---

## 🎯 The Problem & Real-World Impact

In Indian urban residential complexes (RWAs) and apartment societies:
1. **Retail Markup Penalty:** Households buy staples (Rice, Atta, Mustard/Sunflower Oil) individually in small 1 kg – 5 kg packs at retail shops, paying a steep **15% to 25% retail markup**.
2. **WhatsApp Coordination Chaos:** Society management attempts group buys via WhatsApp threads, which quickly collapse into spreadsheet nightmares and untracked requests.
3. **Mismatched Pack Sizes & Waste:** Wholesale vendors deal in bulk 25 kg or 50 kg sacks and 15 L tins. A society needing 710 kg cannot simply order random sacks without causing excess inventory or packaging waste.
4. **Multilingual Merchant Negotiations:** Wholesale Mandi merchants quote over phone or WhatsApp in raw Hinglish, local dialects, and inconsistent pack units. Comparing these manually is exhausting.

### 💡 The Bulkcart Solution
Bulkcart bridges the gap between urban residential demand and wholesale Mandi supply:
- **Aggregates 26+ households** into unified commodity demand with a single click.
- **Normalizes chaotic merchant quotes** (in English, Hindi, and Hinglish) into strictly typed Pydantic models with Google Gemini.
- **Audits quotes deterministically** against government Mandi rates, tagging merchants with clear badges (**`SAHI BHAV`** [Fair Price], **`MEHENGA`** [Expensive], **`SAVDHAN`** [Caution]).
- **Calculates zero-waste commercial sack breakdowns** (e.g., 710 kg rice $\rightarrow$ exactly 28 $\times$ 25 kg + 1 $\times$ 10 kg bags, $0$ kg waste).
- **Generates respectful counter-offers** in Hindi/English and finalizes the round with a perforated **Pakka Bill** resolution receipt slip.

---

## ⚡ How Bulkcart Works

```mermaid
flowchart LR
    A[26 Household Orders\nRice: 710kg | Atta: 425kg | Oil: 150L] --> B[Consolidated Demand]
    C[Unstructured Merchant Quotes\nEnglish / Hindi / Hinglish] --> D[Gemini 2.5 Flash\nPydantic Extraction Engine]
    B --> E[Deterministic Math Engine]
    D --> E
    E --> F[Mandi Price Audit\nSAHI BHAV / MEHENGA Badges]
    E --> G[Zero-Waste Pack Optimizer\nExact Commercial Sack Solver]
    F --> H[Retro Kirana Dashboard]
    G --> H
    H --> I[Pakka Bill Slip\nPerforated Receipt + Counter-Offer]
```

---

## 🎬 60-Second Interactive Demo Guide

Experience the entire proof of concept in four simple steps:

1. **Launch the Dashboard:** Open `http://127.0.0.1:8000` in your browser. You will be greeted by the authentic **Retro Kirana** interface (cream parchment paper, Rozha One typography, and tabular figures).
2. **Click `[📦 Load Sample Round]`:** 
   - Populates 26 verified household demand orders from Gulmohar Enclave RWA (710 kg Sona Masoori Rice, 425 kg Sharbati Atta, 150 L Sunflower Oil).
   - Loads 3 real-world merchant chat quotes from local mandis (Bharat Traders, Kisan Wholesale, Krishna Traders).
3. **Click `[🔍 Analyze Quotes]`:**
   - Watch the live 4-step progress checklist tick through: *Normalizing demand $\rightarrow$ Extracting quotes $\rightarrow$ Auditing against Mandi rates $\rightarrow$ Computing zero-waste sacks*.
   - View the live **Quote Verdict Table** displaying headline savings (**₹16,245 / 18.7% savings** vs retail), per-household dividend (**₹624.81**), and rubber-stamp badges.
   - Inspect the **Commercial Pack Plan** showing exact sack allocations with **0 kg waste**.
4. **Click `[📜 Approve & Send]`:**
   - The screen transitions to an animated, perforated **Pakka Bill** receipt slip with rolling counter ticker and green "SENT" stamp.
   - Click `[📋 Copy Counter-Offer]` to copy the polite Hindi negotiation message ready for WhatsApp dispatch.
   - Click `[↺ Start a New Round]` to reset cleanly.

### 🎥 Official Demo Video & Voiceover Narration

- **Demo Video (MP4, Full HD 1080p, 2m 03s):** [static/bulkcart_demo_video.mp4](static/bulkcart_demo_video.mp4)
- **Audio Voiceover Track (WAV):** [static/bulkcart_voiceover.wav](static/bulkcart_voiceover.wav)
- **Captured Demo Frame Sequence:** [static/demo_frames/](static/demo_frames/)

> The demo video runs for **2 minutes and 3 seconds** (well within the hackathon's 3-minute limit), demonstrating end-to-end functionality from consolidated demand aggregation to the animated Pakka Bill receipt.

---

## 🏗️ System Architecture

Bulkcart enforces a **strict boundary between probabilistic LLM extraction and deterministic arithmetic**:

| Layer | Component | Responsibility |
|---|---|---|
| **Frontend UI** | `static/index.html`<br>`static/style.css`<br>`static/app.js` | Single-page Retro Kirana theme, Rozha One headings, Space Mono tabular numbers, animated rubber-stamp badges, and perforated receipt. Zero external frontend framework dependencies. |
| **API Orchestrator** | `main.py` | FastAPI application exposing `/api/sample-round`, `/api/analyze`, `/api/health`, and static mounts. |
| **LLM Extractor** | `services/llm_extractor.py` | Calls Google Gemini (`gemini-2.5-flash`) with typed `ExtractionResponse` schema. Includes a 10-second timeout guard and resilient zero-failure fallback (`data/cached_fallback.json`). |
| **Audit Math Engine** | `services/math_engine.py` | Pure deterministic Python auditing merchant rates against `data/mandi_benchmark.json` and `data/retail_baseline.json`. Classifies quotes into `SAHI BHAV` ($\le 15\%$), `MEHENGA` ($15\% - 30\%$), or `SAVDHAN` ($> 30\%$). |
| **Pack Optimizer** | `services/pack_optimizer.py` | Mathematical greedy combinatorial solver finding exact sack and tin combinations that satisfy total household demand with $0$ kg/$0$ L waste. |
| **Data Layer** | `data/*.json` | Seeded household orders, Mandi wholesale rates, retail supermarket baselines, and fallback snapshots. |

---

## 🛠️ Tech Stack

- **Backend:** Python 3.10+, [FastAPI](https://fastapi.tiangolo.com/), [Pydantic v2](https://docs.pydantic.dev/), [Uvicorn](https://www.uvicorn.org/)
- **AI / LLM:** [Google GenAI SDK](https://github.com/google-gemini/generative-ai-python) (`google-genai`), Gemini 2.5 Flash with structured response schema
- **Frontend:** Vanilla HTML5, CSS3, modern ES6 JavaScript (No bloated node_modules or Webpack builds)
- **Typography:** Rozha One, Baloo 2, Space Mono, Noto Sans Devanagari (via Google Fonts)
- **Testing:** Pytest & automated Python unit test runners

---

## 🚀 Quick Start & Local Setup

### 1. Clone the Repository
```bash
git clone https://github.com/anshkumarraix-dev/Bulkcart.git
cd Bulkcart
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. (Optional) Configure Gemini API Key
Bulkcart features a **built-in resilient fallback** with pre-extracted sample data so judges and reviewers can test the application **without needing an API key**!

To test live dynamic AI quote extraction, copy the example environment file and add your key:
```bash
cp .env.example .env
# Edit .env and set GEMINI_API_KEY=your_key_here
```

### 4. Run the Application
```bash
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```
Navigate to **`http://127.0.0.1:8000`** in your browser.

---

## 🧪 Testing & Verification

Bulkcart includes automated unit test suites for all core engine slices:

```bash
# Run Slice 1 tests (Math Engine, Mandi Benchmarks, Zero-Waste Pack Optimizer)
python tests/test_slice1.py

# Run Slice 2 tests (Gemini Structured Quote Extraction, Pydantic Schema, Fallback Guard)
python tests/test_slice2.py
```

### Automated Verification Results:
- **Pack Optimizer:** 710 kg Rice $\rightarrow$ 28 $\times$ 25 kg + 1 $\times$ 10 kg bags ($0$ kg waste).
- **Mandi Audit:** Correctly tags Bharat Traders (`MEHENGA`), Kisan Wholesale (`MEHENGA`), and selects Krishna Traders (`SAHI BHAV`).
- **Savings Accuracy:** Validates ₹87,020 retail vs ₹70,775 wholesale = **₹16,245 total savings** (₹624.81 per home).
- **Resilience:** Gracefully falls back to cached baseline when API key is missing or timed out.

---

## 📚 Devpost Learn Skill Pack Artifacts

This project was built following the **Devpost Learn Skill Pack** (`learn-ai-basics`) lifecycle, moving from idea to scope, product definition, technical specification, incremental verification, and shipping:

| Stage | Document | Purpose |
|---|---|---|
| **Scope** | [`devpost/scope.md`](devpost/scope.md) | Initial idea sharpening, core journey definition, and proof-of-concept boundaries. |
| **PRD** | [`devpost/prd.md`](devpost/prd.md) | Complete product requirements, user journeys, edge cases, and feature states. |
| **Spec** | [`devpost/spec.md`](devpost/spec.md) | Technical blueprint, data schemas, API contracts, and architecture decisions. |
| **Checklist** | [`devpost/checklist.md`](devpost/checklist.md) | 4-slice incremental build log with mechanical verification and test records. |
| **App Map** | [`devpost/app-map.html`](devpost/app-map.html) | Standalone interactive visual map and code tour connecting actions to codebase pathways. |

---

## 📂 Repository Structure

```
Bulkcart/
├── data/
│   ├── cached_fallback.json      # Offline fallback extraction data
│   ├── households.json           # 26-household sample orders & merchant quotes
│   ├── mandi_benchmark.json      # Wholesale benchmark rates
│   └── retail_baseline.json      # Supermarket retail price baselines
├── devpost/
│   ├── app-map.html              # Standalone interactive app map & code tour
│   ├── checklist.md              # 4-slice build verification checklist
│   ├── prd.md                    # Product Requirements Document
│   ├── scope.md                  # Project scope & proof of concept boundaries
│   └── spec.md                   # Full Technical Specification
├── services/
│   ├── __init__.py
│   ├── llm_extractor.py          # Gemini extraction with Pydantic schema & fallback
│   ├── math_engine.py            # Mandi audit, badge logic, and savings math
│   └── pack_optimizer.py         # Zero-waste commercial pack combinations
├── static/
│   ├── app.js                    # UI state transitions, checklist timer, Pakka Bill
│   ├── index.html                # Single-page Retro Kirana interface
│   └── style.css                 # Custom CSS, stamps, awnings, receipt animations
├── tests/
│   ├── test_slice1.py            # Pack solver & math engine tests
│   └── test_slice2.py            # Endpoint & extraction resilience tests
├── .env.example                  # Environment configuration template
├── .gitignore                    # Git ignore file (keeps secrets safe)
├── LICENSE                       # MIT Open Source License
├── main.py                       # FastAPI entrypoint & REST endpoints
├── models.py                     # Pydantic data schemas & contracts
├── README.md                     # Interactive project documentation
└── requirements.txt              # Production Python dependencies
```

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details. Built with ❤️ for the **Devpost Learn: Build with AI Basics** Hackathon.
