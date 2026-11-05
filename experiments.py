
import csv
import os
import statistics
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

    # -------------------------------
    # EXPERIMENT 1: WITHOUT CACHING
    # -------------------------------

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

    # -------------------------------
    # EXPERIMENT 2: WITH CACHING
    # -------------------------------

    cached_resolver = DNSResolver(
        ttl=60,
        server_delay=0.1
    )

    cached_times = []

    for domain in requests:

        ip, latency, status = cached_resolver.resolve(
            domain,
            use_cache=True
        )

        cached_times.append(latency)

    # -------------------------------
    # CALCULATE RESULTS
    # -------------------------------

    avg_uncached = statistics.mean(uncached_times)
    avg_cached = statistics.mean(cached_times)

    reduction = (
        (avg_uncached - avg_cached) /
        avg_uncached
    ) * 100

    hit_ratio = (
        cached_resolver.cache_hits /
        len(requests)
    ) * 100

    print("\n====== EXPERIMENTAL RESULTS ======")

    print("Total requests:", len(requests))

    print(
        "Average uncached latency:",
        round(avg_uncached, 3), "ms"
    )

    print(
        "Average cached latency:",
        round(avg_cached, 3), "ms"
    )

    print(
        "Latency reduction:",
        round(reduction, 2), "%"
    )

    print(
        "Cache hit ratio:",
        round(hit_ratio, 2), "%"
    )

    # -------------------------------
    # SAVE DATA TO CSV
    # -------------------------------

    with open(
        "results/latency_results.csv",
        "w",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "Request Number",
            "Domain",
            "Uncached Latency (ms)",
            "Cached Latency (ms)"
        ])

        for i, domain in enumerate(requests):

            writer.writerow([
                i + 1,
                domain,
                round(uncached_times[i], 3),
                round(cached_times[i], 3)
            ])

    # -------------------------------
    # GRAPH 1: AVERAGE LATENCY
    # -------------------------------

    plt.figure(figsize=(7, 5))

    plt.bar(
        ["Without Cache", "With Cache"],
        [avg_uncached, avg_cached]
    )

    plt.ylabel("Average Latency (ms)")
    plt.title("DNS Lookup Latency Comparison")

    plt.savefig("results/latency_comparison.png")
    plt.show()

    # -------------------------------
    # GRAPH 2: CACHE HIT RATIO
    # -------------------------------

    plt.figure(figsize=(7, 5))

    plt.bar(
        ["Cache Hits", "Cache Misses"],
        [
            cached_resolver.cache_hits,
            cached_resolver.cache_misses
        ]
    )

    plt.ylabel("Number of Requests")
    plt.title("DNS Cache Performance")

    plt.savefig("results/cache_performance.png")
    plt.show()

    print("\nFiles saved inside results folder.")
    print("1. latency_results.csv")
    print("2. latency_comparison.png")
    print("3. cache_performance.png")


if __name__ == "__main__":
    run_experiments()
