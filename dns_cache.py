
import time


class DNSCache:

    def __init__(self):
        self.cache = {}

    def get(self, domain):

        if domain not in self.cache:
            return None

        ip, expiry_time = self.cache[domain]

        # Check whether TTL has expired
        if time.monotonic() >= expiry_time:
            del self.cache[domain]
            return None

        return ip

    def put(self, domain, ip, ttl):

        expiry_time = time.monotonic() + ttl

        self.cache[domain] = (ip, expiry_time)

    def display(self):

        print("\n------ DNS CACHE ------")

        if not self.cache:
            print("Cache is empty.")
            return

        current_time = time.monotonic()

        for domain, (ip, expiry) in list(self.cache.items()):

            remaining = expiry - current_time

            if remaining <= 0:
                del self.cache[domain]
                print(domain, "-> EXPIRED")
            else:
                print(
                    domain,
                    "->",
                    ip,
                    "| Remaining TTL:",
                    round(remaining, 2),
                    "seconds"
                )
