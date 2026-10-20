---
doc: checklist
status: approved
---

# Build Checklist

Build mode: fast

## Slices

- [x] **1. Scaffolding, Seed Baselines, and Deterministic Math Engine**
  Becomes usable: A running FastAPI server serving seeded demand data (`/api/sample-round`), plus an independently testable Python engine that solves zero-waste pack combinations and evaluates wholesale benchmarks.
  Why now: Bootstrapping lives inside slice one. It establishes the project files, tests the learner's warm-up (pack optimizer math), and provides the baseline data everything else depends on.
  PRD ref: `prd.md > Features and Behavior > 1. Demand & Quote Loading`, `3. Seeded Baselines & Deterministic Math Engine`, `4. Zero-Waste Pack-Size Optimizer`
  Spec ref: `spec.md > Stack`, `spec.md > File Structure`, `spec.md > Components > 2, 4, 5`
  Build: Create `requirements.txt`, `.env.example`, `models.py`, `data/households.json`, `data/mandi_benchmark.json`, `data/retail_baseline.json`, `data/cached_fallback.json`, `services/pack_optimizer.py`, `services/math_engine.py`, and `main.py` with static mount and `/api/sample-round`.
  Verify (mechanical): Run python test script to verify pack optimizer (710 kg rice → 28×25 + 1×10, 0 waste) and savings math (~₹82,950 baseline vs ~₹68,330 wholesale = ~₹14,620 savings); start uvicorn and verify `GET /api/sample-round` returns 200 with 26 households.
  Learner check: Visit `http://127.0.0.1:8000/api/sample-round` in your browser and confirm the 26-home demand (710 kg rice, 425 kg atta, 150 L oil) loads cleanly as JSON.
  Commit: `Scaffold project and implement deterministic math and pack solver`

- [x] **2. Gemini Structured Quote Extraction and Resilient Fallback**
  Becomes usable: The backend endpoint `POST /api/analyze` parses messy multi-format merchant quotes into verified Pydantic objects and generates a counter-offer, seamlessly falling back to cached JSON on timeout or error.
  Why now: Tackles the primary technical unknown (Pydantic response schema with Gemini) early so the LLM pipeline is proven before building the visual UI.
  PRD ref: `prd.md > Features and Behavior > 2. Live Unstructured Quote Extraction & Strict Schema`, `5. Automated Counter-Offer Generator`, `7. Resilient Demo Fallback`
  Spec ref: `spec.md > Components > 3. LLM Extraction Service`, `spec.md > Data Model`
  Build: Implement `services/llm_extractor.py` using `google-genai` with `ExtractionResponse` schema, `GEMINI_MODEL`, and `API_TIMEOUT_SECONDS = 10`. Wire into `POST /api/analyze` in `main.py` alongside `math_engine` and `pack_optimizer`.
  Verify (mechanical): Send a POST request to `/api/analyze` with the 3 sample merchant texts; verify it returns a 200 with structured items, 3-state badges (`SAHI BHAV`, `MEHENGA`, `SAVDHAN`), pack plan, and counter-offer. Test timeout/disconnect fallback behavior.
  Learner check: Inspect the terminal output showing Gemini extracting structured prices and bag sizes from broken English and Hindi transcripts into Python models.
  Commit: `Implement Gemini structured extraction with cached fallback`

- [ ] **3. Retro Kirana Dashboard and Live Quote Verdict UI**
  Becomes usable: A single-page browser dashboard in the Retro Kirana aesthetic where clicking "Load sample round" populates the inputs, "Analyze quotes" ticks off the 4-step checklist, and the full Quote Verdict table renders with rubber-stamp badges and pack plan.
  Why now: Connects the user experience to the backend pipeline, delivering the core visual interaction and the 1-minute demo kernel.
  PRD ref: `prd.md > Screens and Layout`, `prd.md > Look and Feel`, `prd.md > The Core Journey` (steps 1–5)
  Spec ref: `spec.md > Look and Feel`, `spec.md > Components > 1. Frontend UI`
  Build: Create `static/index.html`, `static/style.css`, and `static/app.js`. Implement Retro Kirana theme (zigzag awning, cream paper, Space Mono tabular numbers, Rozha One headings, rubber-stamp animations, staged 4-step checklist, "Inputs changed" notice, and sample data tag).
  Verify (mechanical): Start server, load `http://127.0.0.1:8000`, click "Load sample round", trigger "Analyze quotes", and verify DOM elements populate with headline savings, 3-state badges, and counter-offer.
  Learner check: Open the dashboard in your browser, click "Load sample round", click "Analyze quotes", watch the 4-step checklist, and verify the side-by-side comparison table.
  Commit: `Build Retro Kirana dashboard and live Quote Verdict UI`

- [ ] **4. Pakka Bill Receipt, Simulated Dispatch, and Complete Journey**
  Becomes usable: Clicking "Approve and send" locks the verdict into an animated, perforated Pakka Bill receipt slip with rolling savings total, red "SENT" stamp, clipboard copy, and reset to empty state.
  Why now: Closes the full journey loop from first arrival to final resolution and round reset.
  PRD ref: `prd.md > The Core Journey` (steps 6–7), `prd.md > Features and Behavior > 6. Pakka Bill Resolution`
  Spec ref: `spec.md > Components > 1. Frontend UI`, `spec.md > The Core Journey Through the System`
  Build: Add Pakka Bill receipt markup and styles to `static/index.html` and `static/style.css` (perforated border, counter animation, stamp bounce). Implement "Approve and send" transition, clipboard copy, "View full verdict" modal/toggle, and "Start a new round" reset in `static/app.js`.
  Verify (mechanical): Click "Approve and send" in browser; verify Pakka Bill renders with dynamic savings, click "Copy counter-offer" and verify clipboard content; click "Start a new round" and verify clean reset to State 1.
  Learner check: Run through the entire 1-minute video demo sequence from empty state to Pakka Bill receipt, copy the counter-offer, and reset.
  Commit: `Add Pakka Bill resolution receipt and complete journey loop`

## Hands-on Checkpoints

- [ ] Early usable behavior explored — Slice 2 (Testing Gemini structured extraction output and fallback)
- [ ] Final kick-the-tires exploration and feedback completed — Slice 4 (Full end-to-end walkthrough)

## Final Review

- [ ] Final review complete — feedback resolved and learner confirms ready to ship

## Code Tour and App Map

- [ ] Learning activity complete — guided route, focused alternative, prior practice connected, or brief recap
- [ ] Optional edit and transfer reflection addressed — offered/declined/already covered/not applicable as appropriate
- [ ] `devpost/app-map.html` generated from finished code, checked, and shown, including a project-grounded practice to reuse

Activity and evidence: [to be recorded upon completion]
Route and stops: [to be recorded upon completion]
Edit outcome: [to be recorded upon completion]
Reflection: [to be recorded upon completion]
Activity mode: [to be recorded upon completion]

## Revisions
