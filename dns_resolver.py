
import time
import random

from dns_cache import DNSCache


class DNSResolver:

    def __init__(self, ttl=10, server_delay=0.1):

        self.cache = DNSCache()
        self.ttl = ttl
        self.server_delay = server_delay

        # Simulated DNS server records
        self.dns_records = {
            "google.com": "142.250.183.14",
            "youtube.com": "142.250.190.46",
            "facebook.com": "157.240.241.35",
            "amazon.com": "205.251.242.103",
            "github.com": "140.82.112.4",
            "openai.com": "104.18.33.45"
        }

        self.total_queries = 0
        self.cache_hits = 0
        self.cache_misses = 0

    def resolve(self, domain, use_cache=True):

        domain = domain.strip().lower()

        start_time = time.perf_counter()

        self.total_queries += 1

        # Step 1: Check cache
        if use_cache:

            cached_ip = self.cache.get(domain)

            if cached_ip is not None:

                self.cache_hits += 1

                latency = (
                    time.perf_counter() - start_time
                ) * 1000

                return cached_ip, latency, "CACHE HIT"

        # Step 2: Cache miss or caching disabled
        if use_cache:
            self.cache_misses += 1

        # Simulate DNS server communication
        time.sleep(
            random.uniform(
                self.server_delay * 0.8,
                self.server_delay * 1.2
            )
        )

        # Step 3: Search DNS server records
        ip = self.dns_records.get(domain)

        if ip is None:

            latency = (
                time.perf_counter() - start_time
            ) * 1000

            return None, latency, "DOMAIN NOT FOUND"

        # Step 4: Store result in cache
        if use_cache:
            self.cache.put(domain, ip, self.ttl)

        latency = (
            time.perf_counter() - start_time
        ) * 1000

        return ip, latency, "CACHE MISS" if use_cache else "UNCACHED"

    def show_statistics(self):

        print("\n====== DNS STATISTICS ======")

        print("Total requests:", self.total_queries)
        print("Cache hits:", self.cache_hits)
        print("Cache misses:", self.cache_misses)

        if self.cache_hits + self.cache_misses > 0:

            hit_ratio = (
                self.cache_hits /
                (self.cache_hits + self.cache_misses)
            ) * 100

            print("Cache hit ratio:", round(hit_ratio, 2), "%")
