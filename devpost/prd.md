---
doc: prd
status: approved
---

# Neighborhood Buying Agent — Product Requirements

An AI buying agent for residential societies that aggregates grocery demand, audits messy merchant quotes against wholesale benchmarks, and optimizes pack sizes so neighborhoods buy like wholesalers.

**Source:** [scope.md > The Unique Kernel](file:///c:/Users/Lenovo/OneDrive/Desktop/AI%20BASICS/devpost/scope.md#L10-L12), [scope.md > Who It's For](file:///c:/Users/Lenovo/OneDrive/Desktop/AI%20BASICS/devpost/scope.md#L13-L15), [scope.md > The POC Boundary](file:///c:/Users/Lenovo/OneDrive/Desktop/AI%20BASICS/devpost/scope.md#L28-L41).

---

## The Core Journey

1. **Initial Arrival (Empty State):** The coordinator opens the web app. The page displays a retro kirana header and top banner: *"Start this week’s buying round"* with a primary **"Load sample round"** button. Below the banner, three panels sit quietly in placeholder states: Demand Summary (*"No orders yet"*), Merchant Quote Inputs (*empty/waiting*), and the Quote Verdict area (*"Your Quote Verdict will appear here"*). The **"Analyze quotes"** button is visible but disabled.
2. **Loading the Round:** The coordinator clicks **"Load sample round"**. The Demand Summary populates with 26 households and consolidated orders:
   - Rice: 710 kg
   - Atta: 425 kg
   - Oil: 150 L
   The three merchant textareas fill with realistic, multi-item unstructured vendor responses: Merchant A (broken English), Merchant B (pasted raw price list), and Merchant C (transcribed Hindi voice note). The **"Analyze quotes"** button activates.
3. **Triggering Analysis (Loading State):** The coordinator clicks **"Analyze quotes"**. The button shifts to a disabled *"Analyzing..."* state. In the Quote Verdict area, a 4-step animated checklist ticks off sequentially:
   - [x] Reading merchant replies
   - [x] Checking against mandi rates
   - [x] Optimizing pack sizes
   - [x] Drafting counter-offer
   *(If the API call fails or exceeds a 10-second timeout, the system automatically triggers the cached fallback response and displays a small "Using saved result (offline demo)" tag).*
4. **Inspecting the Quote Verdict:** When analysis finishes, the Quote Verdict panel presents:
   - **Headline Strip:** *"Best pick: Merchant C · Estimated saving ₹[computed] ([X]%)"* giving the coordinator the decisive answer upfront (computed deterministically in code by comparing total merchant cost against the seeded retail baseline, e.g. ~₹14,600 / ~17%).
   - **Side-by-Side Comparison Table:** Structured columns for Merchants A, B, and C with extracted attributes per item (price per unit, pack sizes offered, price per pack, MOQ, delivery date, payment terms, conditions), color-coded rubber-stamp badges, and a visible *"Sample benchmark data"* tag.
   - **Pack-Size Card:** Zero-waste bulk bag optimization calculated in code for the exact demand:
     - Rice (710 kg): 28 × 25 kg bags + 1 × 10 kg bag = 710 kg (Zero waste).
     - Atta (425 kg): 17 × 25 kg bags = 425 kg (Zero waste).
     - Oil (150 L): 10 × 15 L tins = 150 L (Zero waste).
   - **Editable Counter-Offer:** An LLM-generated message addressed to the best-priced merchant, leveraging the society’s collective volume for extra concession (e.g. free delivery or 2% volume rebate).
   - **Resolution Action:** An **"Approve and send"** primary button.
5. **Editing / Re-Analyzing (Edge State):** If the coordinator modifies any merchant text box after viewing results, a subtle *"Inputs changed, re-analyze"* notice appears, ensuring the LLM only calls when explicitly requested.
6. **Resolving the Round ("Pakka Bill"):** The coordinator clicks **"Approve and send"** (simulated dispatch). The comparison view locks and transforms into a perforated **Pakka Bill** receipt slip displaying:
   - Society header and round date.
   - Final line items, pack breakdown, and delivery schedule.
   - Large rolling-counter total: **"YOU SAVED ₹[computed] ([X]%)"** (calculated dynamically from seed data).
   - Household breakdown: *"₹[computed avg] average per household across 26 homes"*.
   - A tilted, bounced red rubber stamp: **"SENT TO MERCHANT C (Simulated)"**.
   - *"Dhanyavaad!"* footer.
   - Actions: **"Copy counter-offer"** (copies text to clipboard), **"Start a new round"** (resets to empty state), and a **"View full verdict"** toggle to reopen the detailed audit table.

---

## Screens and Layout

A single-page, responsive dashboard split into clear functional sections:

- **App Header:** Retro kirana branding with pure CSS zigzag awning border, title, and one-line tagline.
- **Top Control Banner:** *"Start this week's buying round"* with **"Load sample round"** action.
- **Demand & Inputs Section:**
  - *Demand Summary Card:* Shows total households (26) and consolidated quantities (710 kg rice, 425 kg atta, 150 L oil).
  - *Merchant Quotes Card:* Three side-by-side/stacked editable textareas labeled by format (Broken English, Pasted Price List, Transcribed Hindi Voice Note).
  - *Action Bar:* Prominent **"Analyze quotes"** primary button.
- **Quote Verdict Section:**
  - *Staged Loading Checklist:* Visible during active analysis.
  - *Headline Banner:* Top-line savings & recommended merchant.
  - *Comparison Grid:* Tabular layout comparing extracted quote parameters and fair-price badges.
  - *Pack Optimizer & Counter-Offer:* Two-column split displaying bag breakdown and editable message draft.
  - *Resolution Bar:* **"Approve and send"** button.
- **Pakka Bill Overlay/Card:** Bill-book receipt format with jagged perforated border, rubber-stamp animations, and clipboard/reset controls.

---

## Look and Feel

- **Theme Identity:** *"Retro Kirana"* — the warmth, tactile character, and typography of Indian neighborhood grocery bill-books, street signboards, and truck art.
- **Color Palette:**
  - *Background:* Warm cream paper (`#FDFBF7` / `#F8F4EB`).
  - *Primary Accent:* Marigold yellow (`#F5A623` / `#EAA023`).
  - *Warnings / Overpriced ("MEHENGA"):* Signboard red (`#D32F2F`).
  - *Fair-Price / Success ("SAHI BHAV"):* Peacock teal (`#00897B`).
  - *Caution / Suspiciously Cheap ("SAVDHAN"):* Ochre amber (`#FF8F00`).
  - *Typography / Borders:* Ink-brown (`#2C221E` / `#3E2723`) instead of harsh pure black.
- **Typography:**
  - *Headings & Signboards:* `Rozha One` or `Yatra One` (Google Fonts).
  - *Body Text & UI Labels:* `Baloo 2` (Google Fonts) for friendly, legible interaction.
  - *Hindi Transcripts & Microcopy:* `Noto Sans Devanagari` (Google Fonts).
  - *Prices, Sacks, and Tabular Data:* `Space Mono` or tabular monospace so numbers align like a printed shop invoice.
- **Visual Accents & Motifs:**
  - Pure CSS zigzag awning border atop the dashboard.
  - Hard rectangular outlines (zero border-radius) mirroring physical bill pads.
  - Rubber-stamp badges with bounce animation (*"SAHI BHAV"*, *"MEHENGA"*, *"SAVDHAN"*, *"SENT TO MERCHANT C"*).
  - Subtle perforated CSS line on the Pakka Bill slip.
- **Guardrails:** Comparison table remains crisp, clean, and high-contrast; maximum of one tilted element per panel; all Hindi microcopy paired with clear English subtitles.

---

## Features and Behavior

### 1. Demand & Quote Loading
- Clicking "Load sample round" loads 26 seeded household orders, computes consolidated totals (710 kg rice, 425 kg atta, 150 L oil), and fills the 3 merchant textareas.
- Coordinator can edit any quote text area freely.
- "Analyze quotes" is disabled when quote boxes are empty and enables once text is present.

### 2. Live Unstructured Quote Extraction & Strict Schema
- The LLM extracts an array of structured quote items per merchant using a strict JSON schema:
  ```json
  {
    "merchant_id": "merchant_a | merchant_b | merchant_c",
    "delivery_date": "string | null",
    "payment_terms": "string | null",
    "conditions": "string | null",
    "items": [
      {
        "item_name": "rice | atta | oil",
        "price_per_unit": 0.0,
        "unit": "kg | L",
        "pack_sizes_offered": [25, 10],
        "price_per_pack": [0.0, 0.0],
        "moq": 0
      }
    ]
  }
  ```
- Any unmentioned field is explicitly set to `null` (no hallucinated values). Unstructured caveats or delivery terms flow into `conditions`.

### 3. Seeded Baselines & Deterministic Math Engine
- All math, totals, percentage savings, and badge ratings are calculated **strictly in code**, keeping figures 100% reproducible and defensible. The LLM is restricted to parsing and text generation.
- **Seeded Baselines (JSON):**
  - *Retail Market Baseline:* Average retail prices paid by households at local stores (e.g. Rice: ₹62/kg, Atta: ₹45/kg, Oil: ₹165/L).
  - *Wholesale Mandi Benchmark:* Wholesale reference prices (e.g. Rice: ₹48/kg, Atta: ₹34/kg, Oil: ₹132/L), labeled in UI with *"Sample benchmark data"*.
- **Fair-Price Badge Rules:**
  - **Within ±5% of Mandi Benchmark:** Rubber stamp **"SAHI BHAV"** (Peacock Teal).
  - **> 5% Above Mandi Benchmark:** Rubber stamp **"MEHENGA (+X%)"** (Signboard Red).
  - **< -5% Below Mandi Benchmark:** Rubber stamp **"SAVDHAN (-X%)"** (Ochre Amber caution tag — flags abnormally cheap quotes that may carry hidden condition catches).

### 4. Zero-Waste Pack-Size Optimizer
- Computed in code: uses dynamic programming or greedy combination solver over `pack_sizes_offered` to find the lowest-cost bag combination that satisfies society volume with zero product waste:
  - Rice: 710 kg demand → 28 × 25 kg + 1 × 10 kg bags = 710 kg.
  - Atta: 425 kg demand → 17 × 25 kg bags = 425 kg.
  - Oil: 150 L demand → 10 × 15 L tins = 150 L.

### 5. Automated Counter-Offer Generator
- LLM generates a persuasive, culturally appropriate negotiation draft addressed to the best-rated merchant, citing the society's guaranteed bulk volume (e.g. 710 kg rice) to request waived freight or a closing concession.
- Coordinator can edit the message directly before finalizing.

### 6. Pakka Bill Resolution
- Clicking "Approve and send" locks the state into a simulated sent confirmation bill slip.
- Highlights total society savings (₹18,400 / 13%) and household average (₹320/home).
- "Copy counter-offer" copies negotiation text to clipboard.
- "Start a new round" resets the dashboard to empty state.
- "View full verdict" allows inspecting the underlying comparison table.

### 7. Resilient Demo Fallback
- If the API call fails or times out after 10 seconds, the client instantly loads the pre-cached extraction JSON.
- A discreet tag displays *"Using saved result (offline demo)"* to maintain absolute honesty while keeping video takes flawless.

---

## States and Boundaries

- **State 1: Empty / First Arrival** — Top banner active; Demand, Quotes, and Verdict panels visible in quiet placeholder state; "Analyze" disabled.
- **State 2: Round Loaded** — Demand populated with 26 households; 3 merchant textareas filled with realistic messy text; "Analyze" button active.
- **State 3: Analyzing** — "Analyze" button shows "Analyzing..."; 4-step checklist sequentially checks off in the Verdict panel.
- **State 4: Verdict Rendered** — Headline savings banner displayed; side-by-side audit table, badges, pack card, and editable counter-offer visible.
- **State 5: Inputs Modified** — If merchant text is altered after analysis, an "Inputs changed, re-analyze" notice appears.
- **State 6: Pakka Bill Resolved** — Bill slip rendered with stamped confirmation, rolling savings counter, copy-to-clipboard, reset, and view-verdict controls.
- **State 7: Cached Fallback** — Triggers if API fails or exceeds 10s, displaying *"Using saved result (offline demo)"*.

---

## Product Decisions

- **Deterministic Math in Code:** The LLM parses text and drafts copy, while all financial formulas, badge evaluations, and pack math run in JavaScript to ensure 100% precision.
- **Multi-Item Array Schema:** Models realistic multi-item merchant replies with explicit `null` defaults and `pack_sizes_offered`.
- **Three-State Stamp System:** Covers fair market (`SAHI BHAV`), overpriced (`MEHENGA`), and suspiciously low rates (`SAVDHAN`).
- **Exact Pack-Size Alignment:** Demand tuned to 710 kg rice, 425 kg atta, and 150 L oil to demonstrate true zero-waste optimization.
- **Simulated Dispatch & Honest Fallback:** Labeled clearly in UI and writeup for transparent hackathon judging.

---

## What We're Building (Proof of Concept)

- Single-page responsive web dashboard in Retro Kirana styling.
- Seeded retail baseline and wholesale mandi benchmark JSON files.
- Seeded 26-household demand aggregation display (710 kg rice, 425 kg atta, 150 L oil).
- 3 pre-filled, editable unstructured quote textareas (English, price list, Hindi transcript).
- Staged 4-step loading indicator.
- Live LLM quote parser with strict multi-item array schema.
- Code-based mandi rate benchmark comparison with 3-state rubber-stamp badges.
- Code-based pack-size sack optimization calculator with zero waste.
- Code-based savings calculator comparing best merchant quote to retail baseline.
- Volume-based counter-offer generator with editable text.
- Pakka Bill resolution receipt with animated savings counter and simulated stamp.
- Clipboard copy and full round reset.
- Offline cached fallback with 10s timeout and UI transparency tag.

---

## Deferred From the POC

- **Live Resident Order Intake:** Resident-facing web/mobile forms and QR poster generators.
- **Direct WhatsApp Webhook Integration:** Inbound bot parsing live audio and WhatsApp messages.
- **Live Mandi API:** Real-time government commodity price feeds.
- **Online Payments & Split Billing:** UPI payment collection and escrow distribution.

---

## Non-Goals

- No multi-user login or user session management.
- No backend database or persistent user profiles (session state only).
- No production WhatsApp Business API registration.
- No payment gateway integrations.

---

## Open Questions

*None. Product requirements are locked and ready for technical specification.*
