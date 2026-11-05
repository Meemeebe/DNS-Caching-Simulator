
from dns_resolver import DNSResolver
from experiments import run_experiments
import time


def main():

    resolver = DNSResolver(ttl=10, server_delay=0.1)

    while True:

        print("\n================================")
        print("       DNS CACHING SIMULATOR")
        print("================================")

        print("1. Resolve a domain")
        print("2. Display DNS cache")
        print("3. Change TTL")
        print("4. Display statistics")
        print("5. Wait for TTL expiration")
        print("6. Run performance experiments")
        print("7. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":

            domain = input("Enter domain name: ")

            ip, latency, status = resolver.resolve(domain)

            print("\n------ RESULT ------")
            print("Domain:", domain)
            print("IP Address:", ip if ip else "Not Found")
            print("Status:", status)
            print("Latency:", round(latency, 3), "ms")

        elif choice == "2":

            resolver.cache.display()

        elif choice == "3":

            try:
                new_ttl = float(input("Enter TTL: "))

                if new_ttl <= 0:
                    print("TTL must be positive.")
                else:
                    resolver.ttl = new_ttl
                    print("TTL updated!")

            except ValueError:
                print("Enter a valid number.")

        elif choice == "4":

            resolver.show_statistics()

        elif choice == "5":

            try:
                seconds = float(input("Enter waiting time: "))

                if seconds < 0:
                    print("Invalid waiting time.")
                else:
                    time.sleep(seconds)
                    print("Waiting completed.")

            except ValueError:
                print("Enter a valid number.")

        elif choice == "6":

            run_experiments()

        elif choice == "7":

            print("Thank you for using DNS Simulator!")
            break

        else:

            print("Invalid choice!")


if __name__ == "__main__":
    main()
