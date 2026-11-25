
from flask import Flask, render_template, request, jsonify
from dns_resolver import DNSResolver
from experiments import run_experiments
from flask import send_from_directory
import time

app = Flask(__name__)

# Shared DNS resolver instance
resolver = DNSResolver(ttl=10, server_delay=0.1)


@app.route("/")
def home():
    return render_template("index.html")


# Resolve a domain
@app.route("/api/resolve", methods=["POST"])
def resolve_domain():

    data = request.get_json(silent=True) or {}
    domain = data.get("domain", "").strip()

    if not domain:
        return jsonify({"error": "Please enter a domain name"}), 400

    ip, latency, status = resolver.resolve(domain)

    return jsonify({
        "domain": domain,
        "ip": ip,
        "status": status,
        "latency": round(latency, 3)
    })


# Get DNS statistics
@app.route("/api/stats")
def get_stats():

    total = resolver.total_queries
    hits = resolver.cache_hits
    misses = resolver.cache_misses

    hit_ratio = (
        hits / (hits + misses) * 100
        if hits + misses > 0 else 0
    )

    return jsonify({
        "total_queries": total,
        "cache_hits": hits,
        "cache_misses": misses,
        "hit_ratio": round(hit_ratio, 2)
    })


# Display cache contents
@app.route("/api/cache")
def get_cache():

    current_time = time.monotonic()
    entries = []

    for domain, (ip, expiry) in list(
        resolver.cache.cache.items()
    ):

        remaining = expiry - current_time

        if remaining <= 0:
            del resolver.cache.cache[domain]
            continue

        entries.append({
            "domain": domain,
            "ip": ip,
            "remaining_ttl": round(remaining, 2)
        })

    return jsonify(entries)


# Change TTL
@app.route("/api/config", methods=["POST"])
def update_config():

    data = request.get_json(silent=True) or {}

    try:
        ttl = float(data.get("ttl", 10))
        delay = float(data.get("server_delay", 0.1))

        if ttl <= 0 or delay < 0:
            raise ValueError()

        resolver.ttl = ttl
        resolver.server_delay = delay

        return jsonify({
            "message": "Configuration updated",
            "ttl": ttl,
            "server_delay": delay
        })

    except (ValueError, TypeError):
        return jsonify({
            "error": "Enter a positive TTL and non-negative delay"
        }), 400


# Clear DNS cache
@app.route("/api/cache/clear", methods=["POST"])
def clear_cache():

    resolver.cache.cache.clear()

    return jsonify({
        "message": "DNS cache cleared successfully"
    })

# Run performance experiments
@app.route("/api/experiments", methods=["POST"])
def run_performance_experiments():

    try:
        results = run_experiments()
        return jsonify(results)

    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 500


# Serve generated result files
@app.route("/results/<path:filename>")
def serve_results(filename):

    return send_from_directory("results", filename)


if __name__ == "__main__":
    app.run(debug=True)
