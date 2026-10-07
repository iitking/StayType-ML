/**
 * StayType AI - Modern Frontend Application Script
 */

// Application State
const state = {
    metadata: null,
    selectedBorough: "Manhattan",
    currentPrediction: null,
    history: [],
    radarChart: null,
    probChart: null
};

// Preset Borough Centers
const BOROUGH_COORDS = {
    "Manhattan": { lat: 40.7580, lng: -73.9855, defaultNh: "Midtown" },
    "Brooklyn": { lat: 40.7081, lng: -73.9571, defaultNh: "Williamsburg" },
    "Queens": { lat: 40.7580, lng: -73.8290, defaultNh: "Astoria" },
    "Bronx": { lat: 40.8448, lng: -73.8648, defaultNh: "Riverdale" },
    "Staten Island": { lat: 40.5795, lng: -74.1502, defaultNh: "St. George" }
};

// DOM Content Loaded
document.addEventListener("DOMContentLoaded", async () => {
    initTheme();
    setupSyncInputs();
    setupEventListeners();
    await fetchMetadata();
    setupQuickPresets();
    
    // Run initial prediction with default inputs
    predictStayType();
});

// Theme Management
function initTheme() {
    const savedTheme = localStorage.getItem("staytype-theme") || "dark";
    document.documentElement.setAttribute("data-theme", savedTheme);
    updateThemeIcon(savedTheme);

    const themeToggleBtn = document.getElementById("themeToggleBtn");
    if (themeToggleBtn) {
        themeToggleBtn.addEventListener("click", () => {
            const current = document.documentElement.getAttribute("data-theme");
            const next = current === "dark" ? "light" : "dark";
            document.documentElement.setAttribute("data-theme", next);
            localStorage.setItem("staytype-theme", next);
            updateThemeIcon(next);
            updateChartTheme();
        });
    }
}

function updateThemeIcon(theme) {
    const icon = document.querySelector("#themeToggleBtn i");
    if (!icon) return;
    if (theme === "light") {
        icon.className = "fa-solid fa-moon text-indigo-500 text-lg";
    } else {
        icon.className = "fa-solid fa-sun text-amber-400 text-lg";
    }
}

// Synchronize Sliders with Number Inputs
function setupSyncInputs() {
    const syncPairs = [
        { slider: "priceSlider", input: "priceInput" },
        { slider: "nightsSlider", input: "nightsInput" },
        { slider: "availSlider", input: "availInput" },
        { slider: "reviewsSlider", input: "reviewsInput" },
        { slider: "hostListingsSlider", input: "hostListingsInput" }
    ];

    syncPairs.forEach(pair => {
        const sliderEl = document.getElementById(pair.slider);
        const inputEl = document.getElementById(pair.input);

        if (sliderEl && inputEl) {
            sliderEl.addEventListener("input", (e) => {
                inputEl.value = e.target.value;
                onInputChanged();
            });
            inputEl.addEventListener("input", (e) => {
                sliderEl.value = e.target.value;
                onInputChanged();
            });
        }
    });

    const reviewsPerMonthInput = document.getElementById("reviewsPerMonthInput");
    if (reviewsPerMonthInput) {
        reviewsPerMonthInput.addEventListener("input", onInputChanged);
    }
}

function onInputChanged() {
    updateApiInspector();
}

// Event Listeners Setup
function setupEventListeners() {
    // Form submission
    const form = document.getElementById("listingForm");
    if (form) {
        form.addEventListener("submit", (e) => {
            e.preventDefault();
            predictStayType();
        });
    }

    // Randomize button
    const randomBtn = document.getElementById("randomizeBtn");
    if (randomBtn) {
        randomBtn.addEventListener("click", randomizeInputs);
    }

    // Reset button
    const resetBtn = document.getElementById("resetBtn");
    if (resetBtn) {
        resetBtn.addEventListener("click", resetToDefaults);
    }

    // Copy JSON buttons
    setupCopyButtons();
}

// Fetch Metadata (Boroughs, Neighborhoods, Presets)
async function fetchMetadata() {
    try {
        const res = await fetch("/api/metadata");
        if (!res.ok) throw new Error("Failed to load metadata");
        state.metadata = await res.json();
        
        renderBoroughPills();
        populateNeighborhoods(state.selectedBorough);
    } catch (err) {
        console.error("Error loading metadata:", err);
        showToast("Using fallback data due to metadata fetch error", "warning");
    }
}

// Render Borough Selection Pills
function renderBoroughPills() {
    const container = document.getElementById("boroughPillsContainer");
    if (!container || !state.metadata) return;

    const boroughs = state.metadata.boroughs || Object.keys(BOROUGH_COORDS);
    container.innerHTML = "";

    boroughs.forEach(borough => {
        const pill = document.createElement("button");
        pill.type = "button";
        pill.className = `borough-pill px-3.5 py-2 rounded-xl text-xs font-semibold flex items-center gap-2 transition-all ${
            borough === state.selectedBorough ? "active" : "text-gray-300"
        }`;
        
        const iconClass = getBoroughIcon(borough);
        pill.innerHTML = `<i class="fa-solid ${iconClass}"></i><span>${borough}</span>`;

        pill.addEventListener("click", () => {
            selectBorough(borough);
        });

        container.appendChild(pill);
    });
}

function getBoroughIcon(borough) {
    switch (borough) {
        case "Manhattan": return "fa-city";
        case "Brooklyn": return "fa-bridge-water";
        case "Queens": return "fa-plane-departure";
        case "Bronx": return "fa-baseball-bat-ball";
        case "Staten Island": return "fa-ferry";
        default: return "fa-location-dot";
    }
}

function selectBorough(borough) {
    state.selectedBorough = borough;
    
    // Update pills styling
    const pills = document.querySelectorAll(".borough-pill");
    pills.forEach(pill => {
        if (pill.textContent.includes(borough)) {
            pill.classList.add("active");
            pill.classList.remove("text-gray-300");
        } else {
            pill.classList.remove("active");
            pill.classList.add("text-gray-300");
        }
    });

    populateNeighborhoods(borough);

    // Update coordinates to borough center
    if (BOROUGH_COORDS[borough]) {
        document.getElementById("latInput").value = BOROUGH_COORDS[borough].lat;
        document.getElementById("lngInput").value = BOROUGH_COORDS[borough].lng;
    }

    onInputChanged();
}

function populateNeighborhoods(borough) {
    const select = document.getElementById("neighborhoodSelect");
    if (!select || !state.metadata) return;

    const neighborhoods = (state.metadata.neighborhoods && state.metadata.neighborhoods[borough]) || [];
    select.innerHTML = "";

    neighborhoods.forEach(nh => {
        const opt = document.createElement("option");
        opt.value = nh;
        opt.textContent = nh;
        select.appendChild(opt);
    });

    // Default select
    const defaultNh = BOROUGH_COORDS[borough]?.defaultNh;
    if (defaultNh && neighborhoods.includes(defaultNh)) {
        select.value = defaultNh;
    } else if (neighborhoods.length > 0) {
        select.value = neighborhoods[0];
    }
}

// Preset Quick Buttons
function setupQuickPresets() {
    const container = document.getElementById("quickPresetsContainer");
    if (!container || !state.metadata || !state.metadata.presets) return;

    container.innerHTML = "";

    state.metadata.presets.forEach(preset => {
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-medium bg-white/5 hover:bg-white/10 border border-white/10 hover:border-indigo-500/50 text-gray-200 transition-all hover:scale-105";
        btn.innerHTML = `<i class="fa-solid ${preset.icon || 'fa-tag'} text-indigo-400"></i><span>${preset.name}</span>`;

        btn.addEventListener("click", () => {
            loadPreset(preset);
        });

        container.appendChild(btn);
    });
}

function loadPreset(preset) {
    const d = preset.data;
    selectBorough(d.neighbourhood_group);
    
    setTimeout(() => {
        const nhSelect = document.getElementById("neighborhoodSelect");
        if (nhSelect) nhSelect.value = d.neighbourhood;

        document.getElementById("latInput").value = d.latitude;
        document.getElementById("lngInput").value = d.longitude;

        setSyncValue("price", d.price);
        setSyncValue("nights", d.minimum_nights);
        setSyncValue("avail", d.availability_365);
        setSyncValue("reviews", d.number_of_reviews);
        setSyncValue("hostListings", d.calculated_host_listings_count);
        document.getElementById("reviewsPerMonthInput").value = d.reviews_per_month;

        predictStayType();
        showToast(`Loaded: ${preset.name}`, "info");
    }, 50);
}

function setSyncValue(name, val) {
    const slider = document.getElementById(`${name}Slider`);
    const input = document.getElementById(`${name}Input`);
    if (slider) slider.value = val;
    if (input) input.value = val;
}

// Get current form data
function getFormData() {
    return {
        neighbourhood_group: state.selectedBorough,
        neighbourhood: document.getElementById("neighborhoodSelect").value,
        latitude: parseFloat(document.getElementById("latInput").value) || 40.7580,
        longitude: parseFloat(document.getElementById("lngInput").value) || -73.9855,
        price: parseFloat(document.getElementById("priceInput").value) || 150.0,
        minimum_nights: parseInt(document.getElementById("nightsInput").value) || 2,
        number_of_reviews: parseInt(document.getElementById("reviewsInput").value) || 10,
        reviews_per_month: parseFloat(document.getElementById("reviewsPerMonthInput").value) || 1.2,
        calculated_host_listings_count: parseInt(document.getElementById("hostListingsInput").value) || 1,
        availability_365: parseInt(document.getElementById("availInput").value) || 180
    };
}

// Submit Form to Predict API
async function predictStayType() {
    const submitBtn = document.getElementById("predictBtn");
    const btnSpinner = document.getElementById("btnSpinner");
    const btnText = document.getElementById("btnText");

    try {
        if (submitBtn) submitBtn.disabled = true;
        if (btnSpinner) btnSpinner.classList.remove("hidden");
        if (btnText) btnText.textContent = "Analyzing Listing...";

        const payload = getFormData();
        updateApiInspector(payload, null);

        const res = await fetch("/api/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        if (!res.ok) {
            const errData = await res.json().catch(() => ({}));
            throw new Error(errData.detail || "Prediction request failed.");
        }

        const data = await res.json();
        state.currentPrediction = data;

        renderResults(data);
        updateApiInspector(payload, data);
        addToHistory(data);

        // Confetti for high confidence predictions (> 80%)
        if (data.confidence > 0.80 && typeof confetti === "function") {
            confetti({
                particleCount: 40,
                spread: 60,
                origin: { y: 0.6 }
            });
        }
    } catch (err) {
        console.error("Prediction error:", err);
        showToast(err.message || "Failed to get prediction", "error");
    } finally {
        if (submitBtn) submitBtn.disabled = false;
        if (btnSpinner) btnSpinner.classList.add("hidden");
        if (btnText) btnText.textContent = "Classify Stay Type";
    }
}

// Render Results on Dashboard
function renderResults(data) {
    const resultCard = document.getElementById("resultHeroCard");
    const resultIcon = document.getElementById("resultStayIcon");
    const resultTitle = document.getElementById("resultStayTitle");
    const resultConfidence = document.getElementById("resultConfidenceBadge");
    const resultDescription = document.getElementById("resultStayDescription");
    const resultBestFor = document.getElementById("resultBestForText");

    const stayType = data.predicted_stay_type;
    const details = data.details || {};

    // Remove old glows
    resultCard.classList.remove("theme-glow-emerald", "theme-glow-sky", "theme-glow-amber");

    // Icon & Color styling
    let themeGlowClass = "theme-glow-sky";
    let iconClass = "fa-bed text-sky-400";

    if (stayType === "Entire home/apt") {
        themeGlowClass = "theme-glow-emerald";
        iconClass = "fa-house-chimney text-emerald-400";
    } else if (stayType === "Shared room") {
        themeGlowClass = "theme-glow-amber";
        iconClass = "fa-people-roof text-amber-400";
    }

    resultCard.classList.add(themeGlowClass);
    resultIcon.className = `fa-solid ${iconClass} text-3xl`;
    resultTitle.textContent = details.title || stayType;
    resultConfidence.textContent = `${data.confidence_percentage} Match`;
    resultDescription.textContent = details.description || "";
    resultBestFor.textContent = details.best_for || "";

    // Render Probabilities Bars
    renderProbabilityBars(data.probabilities, stayType);

    // Render Insights
    renderInsights(data.insights);

    // Render Charts
    renderCharts(data);
}

// Render Probability Bars
function renderProbabilityBars(probs, topClass) {
    const container = document.getElementById("probabilityBarsContainer");
    if (!container || !probs) return;

    container.innerHTML = "";

    const classConfig = {
        "Entire home/apt": { label: "Entire Home / Apt", color: "from-emerald-500 to-teal-400", barBg: "bg-emerald-500" },
        "Private room": { label: "Private Room", color: "from-sky-500 to-indigo-500", barBg: "bg-sky-500" },
        "Shared room": { label: "Shared Room", color: "from-amber-500 to-orange-500", barBg: "bg-amber-500" }
    };

    Object.entries(probs).forEach(([cls, prob]) => {
        const pct = (prob * 100).toFixed(1);
        const cfg = classConfig[cls] || { label: cls, color: "from-purple-500 to-indigo-500", barBg: "bg-purple-500" };
        const isWinner = cls === topClass;

        const row = document.createElement("div");
        row.className = "space-y-1.5";
        row.innerHTML = `
            <div class="flex justify-between items-center text-xs font-semibold">
                <span class="flex items-center gap-1.5 ${isWinner ? 'text-white' : 'text-gray-400'}">
                    ${isWinner ? '<i class="fa-solid fa-crown text-amber-400 text-xs"></i>' : ''}
                    ${cfg.label}
                </span>
                <span class="${isWinner ? 'text-indigo-400 font-bold' : 'text-gray-400'}">${pct}%</span>
            </div>
            <div class="w-full bg-white/5 rounded-full h-2.5 overflow-hidden p-0.5 border border-white/5">
                <div class="h-full rounded-full transition-all duration-700 ease-out bg-gradient-to-r ${cfg.color}" style="width: 0%" data-target-width="${pct}%"></div>
            </div>
        `;
        container.appendChild(row);

        // Animate width
        setTimeout(() => {
            const bar = row.querySelector("[data-target-width]");
            if (bar) bar.style.width = bar.getAttribute("data-target-width");
        }, 50);
    });
}

// Render Market Insights
function renderInsights(insights) {
    const list = document.getElementById("insightsList");
    if (!list) return;

    list.innerHTML = "";
    if (!insights || insights.length === 0) {
        list.innerHTML = `<li class="text-xs text-gray-500">No specific market warnings detected.</li>`;
        return;
    }

    insights.forEach(item => {
        const li = document.createElement("li");
        li.className = "flex items-start gap-2.5 text-xs text-gray-300 leading-relaxed";
        li.innerHTML = `
            <i class="fa-solid fa-circle-check text-emerald-400 mt-1 shrink-0"></i>
            <span>${item}</span>
        `;
        list.appendChild(li);
    });
}

// Render Chart.js Visualizations
function renderCharts(data) {
    renderRadarChart(data.input_received);
    renderProbDoughnutChart(data.probabilities);
}

function renderRadarChart(inp) {
    const ctx = document.getElementById("radarChart")?.getContext("2d");
    if (!ctx) return;

    if (state.radarChart) {
        state.radarChart.destroy();
    }

    // Normalized scores out of 100 for visual radar representation
    const priceScore = Math.min(100, Math.round((inp.price / 400) * 100));
    const nightsScore = Math.min(100, Math.round((inp.minimum_nights / 30) * 100));
    const availScore = Math.round((inp.availability_365 / 365) * 100);
    const reviewsScore = Math.min(100, Math.round((inp.number_of_reviews / 150) * 100));
    const hostScaleScore = Math.min(100, Math.round((inp.calculated_host_listings_count / 10) * 100));

    const isDark = document.documentElement.getAttribute("data-theme") !== "light";
    const gridColor = isDark ? "rgba(255, 255, 255, 0.1)" : "rgba(0, 0, 0, 0.1)";
    const textColor = isDark ? "#9ca3af" : "#475569";

    state.radarChart = new Chart(ctx, {
        type: "radar",
        data: {
            labels: ["Nightly Price", "Stay Length", "Year Availability", "Review Density", "Host Portfolio"],
            datasets: [{
                label: "Current Listing",
                data: [priceScore, nightsScore, availScore, reviewsScore, hostScaleScore],
                backgroundColor: "rgba(99, 102, 241, 0.25)",
                borderColor: "#6366f1",
                pointBackgroundColor: "#a855f7",
                pointBorderColor: "#fff",
                pointHoverBackgroundColor: "#fff",
                pointHoverBorderColor: "#6366f1",
                borderWidth: 2
            }, {
                label: "NYC Citywide Median",
                data: [40, 10, 30, 20, 15],
                backgroundColor: "rgba(156, 163, 175, 0.1)",
                borderColor: "rgba(156, 163, 175, 0.4)",
                borderDash: [4, 4],
                borderWidth: 1.5,
                pointRadius: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                r: {
                    angleLines: { color: gridColor },
                    grid: { color: gridColor },
                    pointLabels: {
                        color: textColor,
                        font: { size: 10, family: "'Plus Jakarta Sans', sans-serif" }
                    },
                    ticks: { display: false, max: 100, min: 0 }
                }
            },
            plugins: {
                legend: {
                    position: "bottom",
                    labels: { color: textColor, font: { size: 11 } }
                }
            }
        }
    });
}

function renderProbDoughnutChart(probs) {
    const ctx = document.getElementById("doughnutChart")?.getContext("2d");
    if (!ctx || !probs) return;

    if (state.probChart) {
        state.probChart.destroy();
    }

    const labels = Object.keys(probs);
    const dataValues = Object.values(probs).map(p => (p * 100).toFixed(1));
    const isDark = document.documentElement.getAttribute("data-theme") !== "light";
    const textColor = isDark ? "#9ca3af" : "#475569";

    state.probChart = new Chart(ctx, {
        type: "doughnut",
        data: {
            labels: labels,
            datasets: [{
                data: dataValues,
                backgroundColor: ["#10b981", "#0284c7", "#f59e0b"],
                borderWidth: 0,
                hoverOffset: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: "70%",
            plugins: {
                legend: {
                    position: "bottom",
                    labels: { color: textColor, font: { size: 11 } }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return ` ${context.label}: ${context.raw}%`;
                        }
                    }
                }
            }
        }
    });
}

function updateChartTheme() {
    if (state.currentPrediction) {
        renderCharts(state.currentPrediction);
    }
}

// Update Live API Inspector (JSON and cURL)
function updateApiInspector(payload = null, response = null) {
    const p = payload || getFormData();
    const reqJsonEl = document.getElementById("apiJsonRequest");
    const resJsonEl = document.getElementById("apiJsonResponse");
    const curlEl = document.getElementById("apiCurlSnippet");

    if (reqJsonEl) {
        reqJsonEl.textContent = JSON.stringify(p, null, 2);
    }

    if (resJsonEl && response) {
        resJsonEl.textContent = JSON.stringify(response, null, 2);
    }

    if (curlEl) {
        const curl = `curl -X POST "http://localhost:8000/api/predict" \\
  -H "Content-Type: application/json" \\
  -d '${JSON.stringify(p)}'`;
        curlEl.textContent = curl;
    }
}

// Setup Copy Buttons
function setupCopyButtons() {
    document.querySelectorAll("[data-copy-target]").forEach(btn => {
        btn.addEventListener("click", () => {
            const targetId = btn.getAttribute("data-copy-target");
            const targetEl = document.getElementById(targetId);
            if (!targetEl) return;

            navigator.clipboard.writeText(targetEl.textContent).then(() => {
                const originalHtml = btn.innerHTML;
                btn.innerHTML = `<i class="fa-solid fa-check text-emerald-400"></i> Copied!`;
                setTimeout(() => {
                    btn.innerHTML = originalHtml;
                }, 1800);
            });
        });
    });
}

// Add to Session History
function addToHistory(data) {
    state.history.unshift({
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }),
        stayType: data.predicted_stay_type,
        confidence: data.confidence_percentage,
        borough: data.input_received.neighbourhood_group,
        neighborhood: data.input_received.neighbourhood,
        price: data.input_received.price
    });

    if (state.history.length > 5) {
        state.history.pop();
    }

    renderHistory();
}

function renderHistory() {
    const tbody = document.getElementById("historyTableBody");
    if (!tbody) return;

    if (state.history.length === 0) {
        tbody.innerHTML = `<tr><td colspan="5" class="text-center py-4 text-xs text-gray-500">No predictions recorded yet.</td></tr>`;
        return;
    }

    tbody.innerHTML = "";
    state.history.forEach(item => {
        const tr = document.createElement("tr");
        tr.className = "border-b border-white/5 hover:bg-white/[0.02] text-xs transition-colors";

        let badgeBg = "bg-sky-500/10 text-sky-400 border-sky-500/20";
        if (item.stayType === "Entire home/apt") badgeBg = "bg-emerald-500/10 text-emerald-400 border-emerald-500/20";
        if (item.stayType === "Shared room") badgeBg = "bg-amber-500/10 text-amber-400 border-amber-500/20";

        tr.innerHTML = `
            <td class="py-2.5 px-3 text-gray-400 font-mono">${item.time}</td>
            <td class="py-2.5 px-3">
                <span class="px-2 py-0.5 rounded-full border text-[11px] font-semibold ${badgeBg}">${item.stayType}</span>
            </td>
            <td class="py-2.5 px-3 font-semibold text-gray-200">${item.confidence}</td>
            <td class="py-2.5 px-3 text-gray-300">${item.neighborhood} (${item.borough})</td>
            <td class="py-2.5 px-3 font-mono font-medium text-indigo-400">$${item.price}</td>
        `;
        tbody.appendChild(tr);
    });
}

// Randomize listing inputs
function randomizeInputs() {
    if (!state.metadata) return;

    const boroughs = state.metadata.boroughs || Object.keys(BOROUGH_COORDS);
    const randomBorough = boroughs[Math.floor(Math.random() * boroughs.length)];
    selectBorough(randomBorough);

    setTimeout(() => {
        const nhs = state.metadata.neighborhoods[randomBorough];
        if (nhs && nhs.length > 0) {
            document.getElementById("neighborhoodSelect").value = nhs[Math.floor(Math.random() * nhs.length)];
        }

        const randomPrice = Math.floor(Math.random() * 450) + 25;
        const randomNights = Math.floor(Math.random() * 14) + 1;
        const randomAvail = Math.floor(Math.random() * 365);
        const randomReviews = Math.floor(Math.random() * 120);
        const randomReviewsPerMonth = (Math.random() * 5.5).toFixed(2);
        const randomHostListings = Math.floor(Math.random() * 4) + 1;

        setSyncValue("price", randomPrice);
        setSyncValue("nights", randomNights);
        setSyncValue("avail", randomAvail);
        setSyncValue("reviews", randomReviews);
        setSyncValue("hostListings", randomHostListings);
        document.getElementById("reviewsPerMonthInput").value = randomReviewsPerMonth;

        predictStayType();
        showToast("Generated random NYC listing parameters", "info");
    }, 50);
}

// Reset to default inputs
function resetToDefaults() {
    selectBorough("Manhattan");
    setTimeout(() => {
        document.getElementById("neighborhoodSelect").value = "Midtown";
        setSyncValue("price", 150);
        setSyncValue("nights", 2);
        setSyncValue("avail", 180);
        setSyncValue("reviews", 15);
        setSyncValue("hostListings", 1);
        document.getElementById("reviewsPerMonthInput").value = 1.25;
        document.getElementById("latInput").value = 40.7580;
        document.getElementById("lngInput").value = -73.9855;

        predictStayType();
        showToast("Form reset to default parameters", "info");
    }, 50);
}

// Toast notification helper
function showToast(message, type = "info") {
    const container = document.getElementById("toastContainer");
    if (!container) return;

    const toast = document.createElement("div");
    toast.className = `px-4 py-2.5 rounded-xl shadow-lg border text-xs font-medium flex items-center gap-2 animate-fade-in ${
        type === "error"
            ? "bg-red-950/80 border-red-500/40 text-red-200"
            : type === "warning"
            ? "bg-amber-950/80 border-amber-500/40 text-amber-200"
            : "bg-indigo-950/80 border-indigo-500/40 text-indigo-200"
    }`;

    const icon = type === "error" ? "fa-circle-xmark" : type === "warning" ? "fa-triangle-exclamation" : "fa-circle-info";
    toast.innerHTML = `<i class="fa-solid ${icon}"></i><span>${message}</span>`;

    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = "0";
        toast.style.transform = "translateY(-10px)";
        toast.style.transition = "all 0.3s ease";
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}
