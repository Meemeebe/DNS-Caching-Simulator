
let cacheChart;

// Resolve DNS
async function resolveDomain() {

    const domain = document.getElementById("domainInput").value.trim();
    const result = document.getElementById("lookupResult");

    if (!domain) {
        result.className = "result-box error";
        result.textContent = "Please enter a domain name.";
        return;
    }

    result.textContent = "Resolving domain...";
    result.className = "result-box";

    try {

        const response = await fetch("/api/resolve", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ domain })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Request failed");
        }

        if (!data.ip) {
            result.className = "result-box error";
            result.textContent = `Domain ${data.domain} not found.`;
        } else {

            result.className =
                data.status === "CACHE HIT"
                    ? "result-box hit"
                    : "result-box miss";

            result.innerHTML = `
                <strong>Domain:</strong> ${data.domain}<br>
                <strong>IP Address:</strong> ${data.ip}<br>
                <strong>Status:</strong> ${data.status}<br>
                <strong>Lookup Latency:</strong> ${data.latency} ms
            `;
        }

        document.getElementById("latestLatency").textContent =
            data.latency + " ms";

        await refreshDashboard();

    } catch (error) {

        result.className = "result-box error";
        result.textContent = error.message;

    }
}


// Refresh dashboard statistics
async function refreshDashboard() {

    const response = await fetch("/api/stats");
    const data = await response.json();

    document.getElementById("totalRequests").textContent =
        data.total_queries;

    document.getElementById("cacheHits").textContent =
        data.cache_hits;

    document.getElementById("cacheMisses").textContent =
        data.cache_misses;

    document.getElementById("hitRatio").textContent =
        data.hit_ratio + "%";

    updateChart(data);
    await refreshCache();
}


// Display cache entries
async function refreshCache() {

    const response = await fetch("/api/cache");
    const entries = await response.json();

    const table = document.getElementById("cacheTable");

    if (entries.length === 0) {

        table.innerHTML = `
            <tr>
                <td colspan="3">No cached records yet.</td>
            </tr>
        `;

        return;
    }

    table.innerHTML = entries.map(entry => `
        <tr>
            <td>${entry.domain}</td>
            <td>${entry.ip}</td>
            <td>${entry.remaining_ttl} seconds</td>
        </tr>
    `).join("");
}


// Cache performance graph
function updateChart(data) {

    const values = [data.cache_hits, data.cache_misses];

    if (cacheChart) {

        cacheChart.data.datasets[0].data = values;
        cacheChart.update();

        return;
    }

    const ctx = document.getElementById("cacheChart");

    cacheChart = new Chart(ctx, {

        type: "doughnut",

        data: {

            labels: ["Cache Hits", "Cache Misses"],

            datasets: [{
                data: values,
                backgroundColor: ["#22c55e", "#f59e0b"],
                borderWidth: 0
            }]

        },

        options: {

            responsive: true,

            plugins: {
                legend: {
                    labels: {
                        color: "#cbd5e1"
                    }
                }
            }

        }

    });
}


// Clear cache
async function clearCache() {

    const confirmed = confirm("Are you sure you want to clear DNS cache?");

    if (!confirmed) return;

    await fetch("/api/cache/clear", {
        method: "POST"
    });

    await refreshDashboard();

    alert("DNS cache cleared!");
}


// Update configuration
async function updateConfig() {

    const ttl = document.getElementById("ttlInput").value;
    const delay = document.getElementById("delayInput").value;

    const message = document.getElementById("configMessage");

    try {

        const response = await fetch("/api/config", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                ttl: ttl,
                server_delay: delay
            })

        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error);
        }

        message.textContent = "Configuration updated successfully!";

    } catch (error) {

        message.textContent = error.message;

    }
}


// Enter key support
document.getElementById("domainInput").addEventListener("keydown", event => {

    if (event.key === "Enter") {
        resolveDomain();
    }

});


// Initial dashboard load
refreshDashboard();

// Refresh TTL values periodically
setInterval(refreshCache, 1000);

// RUN EXPERIMENTS AND DISPLAY RESULTS

async function runExperiments() {

    const message = document.getElementById("experimentMessage");

    message.textContent =
        "Running experiments... Please wait while DNS requests are processed.";

    try {

        const response = await fetch("/api/experiments", {
            method: "POST"
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Experiment failed");
        }

        // Show experiment section

        document.getElementById("experimentResults").style.display = "block";

        message.textContent =
            "Experiments completed successfully!";

        // UPDATE SUMMARY CARDS

        document.getElementById("uncachedAvg").textContent =
            data.avg_uncached + " ms";

        document.getElementById("cachedAvg").textContent =
            data.avg_cached + " ms";

        document.getElementById("experimentHitRatio").textContent =
            data.hit_ratio + "%";

        document.getElementById("latencyReduction").textContent =
            data.latency_reduction + "%";

        // DISPLAY GENERATED GRAPHS

        const version = Date.now();

        document.getElementById("latencyGraph").src =
            "/results/latency_comparison.png?v=" + version;

        document.getElementById("cacheGraph").src =
            "/results/cache_performance.png?v=" + version;

        document.getElementById("requestGraph").src =
            "/results/request_latency.png?v=" + version;

        // EXPERIMENTAL COMPARISON TABLE

        document.getElementById("experimentTable").innerHTML = `

            <tr>
                <td>Total Requests</td>
                <td>${data.total_requests}</td>
                <td>${data.total_requests}</td>
            </tr>

            <tr>
                <td>Average Latency</td>
                <td>${data.avg_uncached} ms</td>
                <td>${data.avg_cached} ms</td>
            </tr>

            <tr>
                <td>DNS Server Requests</td>
                <td>${data.total_requests}</td>
                <td>${data.cache_misses}</td>
            </tr>

            <tr>
                <td>Cache Hits</td>
                <td>0</td>
                <td>${data.cache_hits}</td>
            </tr>

            <tr>
                <td>Cache Misses</td>
                <td>Not applicable</td>
                <td>${data.cache_misses}</td>
            </tr>

            <tr>
                <td>Cache Hit Ratio</td>
                <td>0%</td>
                <td>${data.hit_ratio}%</td>
            </tr>

        `;

    } catch (error) {

        message.textContent =
            "Error: " + error.message;

    }

}
