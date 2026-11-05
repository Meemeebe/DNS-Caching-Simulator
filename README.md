
# DNS Resolution and Caching Simulator

A Python-based Computer Networks project that simulates DNS resolution with caching and TTL-based expiration, and analyzes the impact of DNS caching on lookup latency.

## 📌 Project Overview

The Domain Name System (DNS) translates human-readable domain names into their corresponding IP addresses.

Normally, every DNS request requires communication with a DNS server, which introduces lookup latency.

DNS caching improves performance by temporarily storing previously resolved domain names and their IP addresses.

This project implements a simplified DNS resolver with a caching mechanism and Time To Live (TTL) expiration to compare the performance of cached and uncached DNS requests.

## 🎯 Objectives

- Understand the working of DNS resolution.
- Implement a simplified DNS resolver.
- Implement DNS caching to store resolved domain names and IP addresses.
- Implement TTL-based cache expiration.
- Measure DNS lookup latency.
- Compare cached and uncached DNS requests.
- Analyze performance using experimental results and graphs.

## ✨ Features

- DNS resolution simulation.
- DNS cache implementation.
- Cache hit and cache miss detection.
- TTL-based cache expiration.
- Configurable TTL values.
- DNS lookup latency measurement.
- Cache performance statistics.
- Cached vs. uncached performance comparison.
- Experimental data export in CSV format.
- Graph generation using Matplotlib.

## 🛠️ Technologies Used

- Python 3
- Matplotlib
- Pandas
- CSV
- VS Code

## 📂 Project Structure

DNS_Caching_Simulator/
│
├── main.py
├── dns_resolver.py
├── dns_cache.py
├── experiments.py
├── README.md
├── .gitignore
│
└── results/
    ├── latency_results.csv
    ├── latency_comparison.png
    └── cache_performance.png

## ⚙️ Installation and Setup

### 1. Clone the repository

git clone https://github.com/USERNAME/DNS-Caching-Simulator.git

### 2. Navigate to the project folder

cd DNS-Caching-Simulator

### 3. Install dependencies

python -m pip install matplotlib pandas

### 4. Run the simulator

python main.py

## 🚀 How to Use

The simulator provides an interactive menu with the following options:

1. Resolve a domain
2. Display DNS cache
3. Change TTL
4. Display statistics
5. Wait for TTL expiration
6. Run performance experiments
7. Exit

### Example Domains

- google.com
- youtube.com
- facebook.com
- amazon.com
- github.com
- openai.com

## 🧪 Experimental Analysis

The project compares DNS lookup performance under two conditions:

### Without DNS Caching
Every request is sent to the simulated DNS server, resulting in repeated lookup delays.

### With DNS Caching
Previously resolved domain names are retrieved directly from the cache if their TTL has not expired.

### Performance Metrics

- Average DNS lookup latency
- Cache hit ratio
- Cache miss ratio
- Number of DNS server queries
- Percentage reduction in lookup latency

## 📊 Experimental Results

The experiments generate the following files:

| File | Description |
|---|---|
| latency_results.csv | Request-wise latency data |
| latency_comparison.png | Cached vs. uncached latency graph |
| cache_performance.png | Cache hits vs. misses graph |

## 📖 Concepts Demonstrated

- Domain Name System (DNS)
- DNS Resolution
- DNS Caching
- Cache Hit and Cache Miss
- Time To Live (TTL)
- Lookup Latency
- Performance Analysis

## ⚠️ Limitations

- Uses a simulated DNS server rather than actual recursive DNS servers.
- DNS records are predefined.
- Network delays are simulated.
- Results may vary depending on system performance.

## 🎓 Conclusion

The project demonstrates how DNS caching reduces lookup latency by avoiding repeated communication with DNS servers.

TTL-based expiration ensures that cached records are not retained indefinitely, allowing fresh DNS lookups when entries expire.

The experimental comparison highlights the performance benefits of DNS caching in network communication.

---

**Project:** Computer Networks Assignment  
**Topic:** DNS Resolution and Caching Simulator
