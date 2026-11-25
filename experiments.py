
import csv
import os
import statistics

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt

from dns_resolver import DNSResolver


def run_experiments():

    os.makedirs("results", exist_ok=True)

    domains = [
        "google.com",
        "youtube.com",
        "facebook.com",
        "amazon.com",
        "github.com"
    ]

    requests = domains * 10

    # EXPERIMENT 1: WITHOUT CACHE

    uncached_resolver = DNSResolver(
        ttl=60,
        server_delay=0.1
    )

    uncached_times = []

    for domain in requests:

        ip, latency, status = uncached_resolver.resolve(
            domain,
            use_cache=False
        )

        uncached_times.append(latency)

    # EXPERIMENT 2: WITH CACHE

    cached_resolver = DNSResolver(
        ttl=60,
        server_delay=0.1
    )

    cached_times = []
    statuses = []

    for domain in requests:

        ip, latency, status = cached_resolver.resolve(
            domain,
            use_cache=True
        )

        cached_times.append(latency)
        statuses.append(status)

    # CALCULATE STATISTICS

    avg_uncached = statistics.mean(uncached_times)
    avg_cached = statistics.mean(cached_times)

    reduction = (
        (avg_uncached - avg_cached) /
        avg_uncached * 100
    ) if avg_uncached > 0 else 0

    hits = cached_resolver.cache_hits
    misses = cached_resolver.cache_misses

    hit_ratio = hits / len(requests) * 100
    miss_ratio = misses / len(requests) * 100

    # SAVE CSV

    csv_path = "results/latency_results.csv"

    with open(csv_path, "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            "Request Number",
            "Domain",
            "Uncached Latency (ms)",
            "Cached Latency (ms)",
            "Cache Status"
        ])

        for i, domain in enumerate(requests):

            writer.writerow([
                i + 1,
                domain,
                round(uncached_times[i], 3),
                round(cached_times[i], 3),
                statuses[i]
            ])

    # GRAPH 1: AVERAGE LATENCY

    plt.figure(figsize=(8, 5))

    plt.bar(
        ["Without Cache", "With Cache"],
        [avg_uncached, avg_cached]
    )

    plt.ylabel("Average Latency (ms)")
    plt.title("DNS Lookup Latency Comparison")

    plt.tight_layout()
    plt.savefig("results/latency_comparison.png", dpi=150)
    plt.close()

    # GRAPH 2: CACHE PERFORMANCE

    plt.figure(figsize=(7, 5))

    plt.bar(
        ["Cache Hits", "Cache Misses"],
        [hits, misses]
    )

    plt.ylabel("Number of Requests")
    plt.title("DNS Cache Performance")

    plt.tight_layout()
    plt.savefig("results/cache_performance.png", dpi=150)
    plt.close()

    # GRAPH 3: REQUEST-WISE LATENCY

    plt.figure(figsize=(10, 5))

    plt.plot(
        range(1, len(requests) + 1),
        uncached_times,
        label="Without Cache",
        marker="."
    )

    plt.plot(
        range(1, len(requests) + 1),
        cached_times,
        label="With Cache",
        marker="."
    )

    plt.xlabel("Request Number")
    plt.ylabel("Latency (ms)")
    plt.title("Request-wise DNS Latency")
    plt.legend()

    plt.tight_layout()
    plt.savefig("results/request_latency.png", dpi=150)
    plt.close()

    # RETURN RESULTS TO FLASK

    return {
        "total_requests": len(requests),
        "cache_hits": hits,
        "cache_misses": misses,
        "hit_ratio": round(hit_ratio, 2),
        "miss_ratio": round(miss_ratio, 2),
        "avg_uncached": round(avg_uncached, 3),
        "avg_cached": round(avg_cached, 3),
        "latency_reduction": round(reduction, 2),

        "uncached_times": [
            round(x, 3) for x in uncached_times
        ],

        "cached_times": [
            round(x, 3) for x in cached_times
        ],

        "domains": requests,
        "statuses": statuses
    }


if __name__ == "__main__":

    results = run_experiments()

    print("\nEXPERIMENT RESULTS")
    print(results)

    print("\nGraphs and CSV saved in results/")
