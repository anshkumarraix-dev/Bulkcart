// ==========================================================================
// Neighborhood Buying Agent — Frontend State Machine & Controller
// ==========================================================================

document.addEventListener("DOMContentLoaded", () => {
  // State elements
  const loadSampleBtn = document.getElementById("load-sample-btn");
  const analyzeBtn = document.getElementById("analyze-btn");
  const approveSendBtn = document.getElementById("approve-send-btn");
  const copyOfferBtn = document.getElementById("copy-offer-btn");
  const viewVerdictToggleBtn = document.getElementById("view-verdict-toggle-btn");
  const resetRoundBtn = document.getElementById("reset-round-btn");

  const demandEmptyState = document.getElementById("demand-empty-state");
  const demandLoadedContent = document.getElementById("demand-loaded-content");
  const demandBadge = document.getElementById("demand-badge");
  const householdTableBody = document.getElementById("household-table-body");

  const merchantAText = document.getElementById("merchant-a-text");
  const merchantBText = document.getElementById("merchant-b-text");
  const merchantCText = document.getElementById("merchant-c-text");
  const inputsChangedBanner = document.getElementById("inputs-changed-banner");

  const verdictEmptyState = document.getElementById("verdict-empty-state");
  const verdictLoadingState = document.getElementById("verdict-loading-state");
  const verdictResults = document.getElementById("verdict-results");
  const pakkaBillContainer = document.getElementById("pakka-bill-container");
  const fallbackDisclaimer = document.getElementById("fallback-disclaimer");
  const fallbackReasonText = document.getElementById("fallback-reason-text");

  let currentVerdictData = null;
  let hasAnalyzedOnce = false;

  // --------------------------------------------------------------------------
  // 1. Load Sample Round Data
  // --------------------------------------------------------------------------
  loadSampleBtn.addEventListener("click", async () => {
    loadSampleBtn.disabled = true;
    loadSampleBtn.innerHTML = "Loading Round...";

    try {
      const res = await fetch("/api/sample-round");
      if (!res.ok) throw new Error("Failed to load sample round data");
      const data = await res.json();

      // Populate Demand Summary
      document.getElementById("society-name-display").textContent = data.society_name;
      document.getElementById("household-count-display").textContent = `${data.total_households} Participating Homes`;

      // Demand Quantities
      data.demand.forEach(item => {
        if (item.item_name === "rice") document.getElementById("demand-rice-qty").innerHTML = `${item.quantity} <small>kg</small>`;
        if (item.item_name === "atta") document.getElementById("demand-atta-qty").innerHTML = `${item.quantity} <small>kg</small>`;
        if (item.item_name === "oil") document.getElementById("demand-oil-qty").innerHTML = `${item.quantity} <small>L</small>`;
      });

      // Render 26 households
      householdTableBody.innerHTML = "";
      data.households.forEach(h => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td><strong>${h.flat_no}</strong></td>
          <td>${h.resident_name}</td>
          <td>${h.rice_kg} kg</td>
          <td>${h.atta_kg} kg</td>
          <td>${h.oil_l} L</td>
        `;
        householdTableBody.appendChild(tr);
      });

      // Switch demand state
      demandEmptyState.classList.add("hidden");
      demandLoadedContent.classList.remove("hidden");
      demandBadge.className = "pill-badge pill-active";
      demandBadge.textContent = "26 Homes Ready";

      // Populate 3 Merchant Textareas
      merchantAText.value = data.sample_quotes.merchant_a || "";
      merchantBText.value = data.sample_quotes.merchant_b || "";
      merchantCText.value = data.sample_quotes.merchant_c || "";

      // Enable Analyze Button
      analyzeBtn.disabled = false;
      analyzeBtn.classList.remove("btn-secondary");
      analyzeBtn.classList.add("btn-action");

      loadSampleBtn.disabled = false;
      loadSampleBtn.innerHTML = '<span class="btn-icon">✓</span> Round Loaded';
      setTimeout(() => {
        loadSampleBtn.innerHTML = '<span class="btn-icon">📦</span> Reload Sample Data';
      }, 2000);

    } catch (err) {
      console.error(err);
      alert("Error loading sample data: " + err.message);
      loadSampleBtn.disabled = false;
      loadSampleBtn.innerHTML = '<span class="btn-icon">📦</span> Load Sample Round';
    }
  });

  // --------------------------------------------------------------------------
  // 2. Track Custom Input Edits
  // --------------------------------------------------------------------------
  [merchantAText, merchantBText, merchantCText].forEach(textarea => {
    textarea.addEventListener("input", () => {
      if (hasAnalyzedOnce) {
        inputsChangedBanner.classList.remove("hidden");
      }
      if (merchantAText.value.trim() || merchantBText.value.trim() || merchantCText.value.trim()) {
        analyzeBtn.disabled = false;
      }
    });
  });

  // --------------------------------------------------------------------------
  // 3. Staged 4-Step Checklist Runner
  // --------------------------------------------------------------------------
  function runStagedChecklist(onComplete) {
    const steps = [
      document.getElementById("step-1"),
      document.getElementById("step-2"),
      document.getElementById("step-3"),
      document.getElementById("step-4")
    ];

    // Reset steps
    steps.forEach(s => {
      s.className = "checklist-item pending";
    });

    let currentStepIndex = 0;

    function advance() {
      if (currentStepIndex > 0) {
        steps[currentStepIndex - 1].className = "checklist-item completed";
      }
      if (currentStepIndex < steps.length) {
        steps[currentStepIndex].className = "checklist-item active";
        currentStepIndex++;
        setTimeout(advance, 600); // 600ms per step animation
      } else {
        setTimeout(onComplete, 400);
      }
    }

    advance();
  }

  // --------------------------------------------------------------------------
  // 4. Analyze Quotes Action
  // --------------------------------------------------------------------------
  analyzeBtn.addEventListener("click", async () => {
    analyzeBtn.disabled = true;
    analyzeBtn.innerHTML = '<span class="btn-icon">⏳</span> Analyzing Reasoning Pipeline...';

    // UI State: show loading checklist
    verdictEmptyState.classList.add("hidden");
    verdictResults.classList.add("hidden");
    pakkaBillContainer.classList.add("hidden");
    verdictLoadingState.classList.remove("hidden");
    inputsChangedBanner.classList.add("hidden");

    const payload = {
      merchant_a_text: merchantAText.value,
      merchant_b_text: merchantBText.value,
      merchant_c_text: merchantCText.value
    };

    let apiResponse = null;
    let apiError = null;

    // Trigger API call concurrently with staged animation
    const fetchPromise = fetch("/api/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    })
      .then(res => {
        if (!res.ok) throw new Error("API call returned " + res.status);
        return res.json();
      })
      .then(data => { apiResponse = data; })
      .catch(err => { apiError = err; });

    // Run staged visual checklist (takes ~2.5 seconds total)
    runStagedChecklist(async () => {
      // Await fetch if still running
      await fetchPromise;

      verdictLoadingState.classList.add("hidden");
      analyzeBtn.disabled = false;
      analyzeBtn.innerHTML = '<span class="btn-icon">⚡</span> Analyze Quotes with AI';

      if (apiError || !apiResponse) {
        console.error("Analysis error:", apiError);
        alert("Analysis failed. Please ensure the backend is running.");
        return;
      }

      currentVerdictData = apiResponse;
      hasAnalyzedOnce = true;
      renderVerdict(apiResponse);
    });
  });

  // --------------------------------------------------------------------------
  // 5. Render Quote Verdict
  // --------------------------------------------------------------------------
  function renderVerdict(data) {
    verdictResults.classList.remove("hidden");

    // Fallback indicator
    if (data.used_fallback) {
      fallbackDisclaimer.classList.remove("hidden");
      fallbackReasonText.textContent = data.fallback_warning || "Running in offline demo mode";
    } else {
      fallbackDisclaimer.classList.add("hidden");
    }

    // Headline Strip
    document.getElementById("verdict-best-merchant-name").textContent = `${data.best_merchant_name} (${data.best_merchant_id.replace('_', ' ').toUpperCase()})`;
    document.getElementById("verdict-total-saving").textContent = Number(data.total_estimated_saving).toLocaleString('en-IN');
    document.getElementById("verdict-saving-pct").textContent = `(${data.saving_percentage}% cut)`;
    document.getElementById("verdict-per-home-saving").textContent = `Avg ₹${Number(data.per_household_saving).toLocaleString('en-IN')} saved per household across 26 flats`;

    // Comparison Table Columns & Badges
    const auditsMap = {};
    data.merchant_audits.forEach(a => { auditsMap[a.merchant_id] = a; });

    const quotesMap = {};
    data.quotes.forEach(q => { quotesMap[q.merchant_id] = q; });

    // Render Stamps
    ['merchant_a', 'merchant_b', 'merchant_c'].forEach(mid => {
      const audit = auditsMap[mid];
      const stampEl = document.getElementById(`stamp-${mid.replace('_', '-')}`);
      if (audit && stampEl) {
        let badgeClass = "stamp-fair";
        if (audit.badge_type === "expensive") badgeClass = "stamp-expensive";
        if (audit.badge_type === "caution") badgeClass = "stamp-caution";
        stampEl.innerHTML = `<div class="rubber-stamp ${badgeClass}">${audit.badge_label}</div>`;
      }
    });

    // Populate Pricing & Terms
    function getPriceStr(quote, itemName) {
      if (!quote || !quote.items) return "—";
      const it = quote.items.find(i => i.item_name.toLowerCase().includes(itemName));
      if (!it) return "—";
      const packStr = it.pack_sizes_offered && it.pack_sizes_offered.length ? `(${it.pack_sizes_offered.join('/')}${it.unit} bags)` : "";
      return `₹${it.price_per_unit}/${it.unit} <small>${packStr}</small>`;
    }

    ['a', 'b', 'c'].forEach(letter => {
      const mid = `merchant_${letter}`;
      const q = quotesMap[mid];
      const aud = auditsMap[mid];

      const priceRiceEl = document.getElementById(`price-rice-${letter}`);
      if (priceRiceEl) priceRiceEl.innerHTML = getPriceStr(q, 'rice');

      const priceAttaEl = document.getElementById(`price-atta-${letter}`);
      if (priceAttaEl) priceAttaEl.innerHTML = getPriceStr(q, 'atta');

      const priceOilEl = document.getElementById(`price-oil-${letter}`);
      if (priceOilEl) priceOilEl.innerHTML = getPriceStr(q, 'oil');

      const delEl = document.getElementById(`delivery-${letter}`);
      if (delEl) delEl.textContent = q ? (q.delivery_date || "—") : "—";

      const termsEl = document.getElementById(`terms-${letter}`);
      if (termsEl) termsEl.textContent = q ? (q.payment_terms || "—") : "—";

      const condEl = document.getElementById(`cond-${letter}`);
      if (condEl) condEl.textContent = q ? (q.conditions || "None specified") : "—";

      const totalEl = document.getElementById(`total-cost-${letter}`);
      if (totalEl && aud) totalEl.textContent = `₹${Number(aud.total_cost).toLocaleString('en-IN')}`;
    });

    // Pack Plans
    const packPlansList = document.getElementById("pack-plans-list");
    packPlansList.innerHTML = "";
    data.pack_plans.forEach(plan => {
      const row = document.createElement("div");
      row.className = "pack-plan-row";
      row.innerHTML = `
        <span class="pack-item-name">${plan.item_name} (${plan.demand_qty} ${plan.unit}):</span>
        <span class="pack-breakdown-val">${plan.sacks_breakdown} <span class="zero-waste-tag">Zero Waste</span></span>
      `;
      packPlansList.appendChild(row);
    });

    // Counter Offer
    document.getElementById("counter-offer-textarea").value = data.counter_offer_draft || "";
  }

  // --------------------------------------------------------------------------
  // 6. Approve & Generate Pakka Bill
  // --------------------------------------------------------------------------
  approveSendBtn.addEventListener("click", () => {
    if (!currentVerdictData) return;

    verdictResults.classList.add("hidden");
    pakkaBillContainer.classList.remove("hidden");

    const data = currentVerdictData;
    const bestQuote = data.quotes.find(q => q.merchant_id === data.best_merchant_id) || data.quotes[0];

    // Populate Pakka Bill Items
    const billItemsBody = document.getElementById("bill-items-body");
    billItemsBody.innerHTML = "";

    const demandMap = { "rice": "710 kg", "atta": "425 kg", "oil": "150 L" };

    if (bestQuote && bestQuote.items) {
      bestQuote.items.forEach(item => {
        const plan = data.pack_plans.find(p => p.item_name.toLowerCase().includes(item.item_name.toLowerCase()));
        const breakdown = plan ? plan.sacks_breakdown : (demandMap[item.item_name] || "");
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td><strong>${item.item_name.toUpperCase()}</strong> (${bestQuote.merchant_name})</td>
          <td>${breakdown}</td>
          <td>₹${item.price_per_unit}/${item.unit}</td>
          <td class="text-right">₹${Number(item.price_per_unit * (plan ? plan.demand_qty : 1)).toLocaleString('en-IN')}</td>
        `;
        billItemsBody.appendChild(tr);
      });
    }

    // Totals
    document.getElementById("bill-retail-total").textContent = `₹${Number(data.total_retail_cost).toLocaleString('en-IN')}`;
    document.getElementById("bill-wholesale-total").textContent = `₹${Number(data.best_merchant_cost).toLocaleString('en-IN')}`;
    document.getElementById("bill-savings-text").textContent = `YOU SAVED ₹${Number(data.total_estimated_saving).toLocaleString('en-IN')} (${data.saving_percentage}%)`;
    document.getElementById("bill-avg-home-text").textContent = `Average ₹${Number(data.per_household_saving).toLocaleString('en-IN')} saved per household across 26 flats`;

    // Scroll to bill
    pakkaBillContainer.scrollIntoView({ behavior: 'smooth' });
  });

  // --------------------------------------------------------------------------
  // 7. Clipboard Copy
  // --------------------------------------------------------------------------
  copyOfferBtn.addEventListener("click", () => {
    const textToCopy = document.getElementById("counter-offer-textarea").value;
    navigator.clipboard.writeText(textToCopy).then(() => {
      const origText = copyOfferBtn.innerHTML;
      copyOfferBtn.innerHTML = "✅ Counter-Offer Copied to Clipboard!";
      setTimeout(() => { copyOfferBtn.innerHTML = origText; }, 2500);
    }).catch(err => {
      alert("Clipboard copy failed. Please select text manually.");
    });
  });

  // --------------------------------------------------------------------------
  // 8. Toggle Full Verdict View from Pakka Bill
  // --------------------------------------------------------------------------
  viewVerdictToggleBtn.addEventListener("click", () => {
    if (verdictResults.classList.contains("hidden")) {
      verdictResults.classList.remove("hidden");
      viewVerdictToggleBtn.innerHTML = "🙈 Hide Audit Table";
      verdictResults.scrollIntoView({ behavior: 'smooth' });
    } else {
      verdictResults.classList.add("hidden");
      viewVerdictToggleBtn.innerHTML = "🔍 View Full Audit Verdict";
    }
  });

  // --------------------------------------------------------------------------
  // 9. Reset Round
  // --------------------------------------------------------------------------
  resetRoundBtn.addEventListener("click", () => {
    if (!confirm("Are you sure you want to reset to a clean round?")) return;

    // Reset state
    hasAnalyzedOnce = false;
    currentVerdictData = null;

    demandEmptyState.classList.remove("hidden");
    demandLoadedContent.classList.add("hidden");
    demandBadge.className = "pill-badge pill-neutral";
    demandBadge.textContent = "Waiting";

    merchantAText.value = "";
    merchantBText.value = "";
    merchantCText.value = "";
    inputsChangedBanner.classList.add("hidden");
    analyzeBtn.disabled = true;

    verdictEmptyState.classList.remove("hidden");
    verdictLoadingState.classList.add("hidden");
    verdictResults.classList.add("hidden");
    pakkaBillContainer.classList.add("hidden");

    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

});
