---
doc: scope
status: approved
---

# Neighborhood Buying Agent

An AI buying agent for residential societies that aggregates grocery demand, audits messy merchant quotes against wholesale benchmarks, and optimizes pack sizes so neighborhoods buy like wholesalers.

## The Unique Kernel
The **Quote Verdict** pipeline: transforming multiple messy, multi-format merchant replies (broken English, pasted raw price lists, transcribed Hindi voice notes) into structured side-by-side pricing, auditing them against mandi wholesale benchmarks with fair-price badges, solving pack-size combinations to cut waste, and generating a volume-leveraged counter-offer in seconds.

## Who It's For
The **Residential Society Buying Coordinator**—the resident or volunteer managing collective purchasing who currently suffers through chaotic WhatsApp threads, manual tallying, and chasing vendors without real pricing transparency or leverage.

## The Core Loop
The coordinator loads the week's buying round, reviews the consolidated society demand, pastes or edits incoming merchant replies, and runs the AI Quote Verdict. The AI parses the quotes, checks them against mandi rates, optimizes pack sizes, and drafts a counter-offer. The coordinator reviews the verdict, makes the final call, and shares visible savings with the society.

## Inspiration & Identity
Pragmatic local commerce with radical pricing transparency. A clean, utilitarian dashboard that turns chaotic unstructured text into clear, authoritative financial decisions with zero guesswork.

## Why This Matters to the Learner
A chance to build a complete, functional AI-driven product where the AI handles real unstructured reasoning and optimization, while the human retains full decision ownership—practicing API integration, structured outputs, and clean application design from scratch.

## What "Working" Looks Like
A single-screen coordinator dashboard running locally. Clicking "Load sample round" populates 26 seeded household orders and the consolidated society demand (710 kg rice, 425 kg atta, 150 L oil). Three editable input boxes hold messy vendor quotes. Clicking "Analyze quotes" triggers live AI parsing, displaying a side-by-side comparison table, benchmark audit badges with a visible "Sample benchmark data" label ("Merchant B: 9% above mandi rate. Merchant C: fair"), the pack-size combination (28×25 kg + 1×10 kg bags), an editable ready-to-send counter-offer, and the dynamically calculated headline savings. A cached fallback response ensures the demo runs smoothly during video recording even if the API or network hiccups.

## The POC Boundary (Now)
- Single-screen coordinator dashboard.
- "Load sample round" button populating 26 seeded household orders and consolidated demand.
- 3 editable text boxes pre-filled with messy merchant replies (broken English, pasted price list, transcribed Hindi note).
- Live LLM parsing of unstructured quotes into structured price, delivery, and condition fields.
- Mandi benchmark comparison logic rendering fair-price badges, labeled with "Sample benchmark data".
- Pack-size optimizer calculating the cheapest combination of bulk sacks (e.g. 25 kg and 10 kg) with zero waste.
- AI-generated counter-offer draft using collective order volume as bargaining leverage.
- Dynamic recalculation of savings and verdict when quote inputs are edited.
- Single "Approve and send" resolution state showing final savings.
- Cached fallback response for resilient live video recording without network risk.

## Later
- Lightweight household ordering portal with shareable society codes and printable QR invite posters.
- Live WhatsApp bot / webhook integration for inbound voice notes and merchant quote intake.
- Real-time Mandi price API integration replacing sample wholesale benchmarks.
- Merchant-facing order acceptance and confirmation portal.
- Split-payment collection and society delivery tracking.

## Explicitly Cut
- **Multi-user authentication and resident accounts:** Adds user management plumbing without improving the core AI reasoning demonstration.
- **Direct WhatsApp API / SMS gateways:** High setup friction, webhook hosting, and credential requirements that distract from the 2–4 hour hackathon core.
- **Payment processing and escrow:** Complex financial integration unnecessary for validating demand aggregation and quote negotiation.
