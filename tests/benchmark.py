import time
import json
from src.user_model import UserModel

def run_benchmark(iterations: int = 10_000):
    sample_payload = json.dumps({
        "id": 100,
        "username": "BenchmarkUser",
        "email": "bench@company.org",
        "address": {"street": "100 Speed Way", "city": "FastCity", "postal_code": "12345"},
        "profile": {"interests": ["benchmarking", "python"]}
    })

    start_time = time.perf_counter()
    for _ in range(iterations):
        _ = UserModel.parse_from_json_str(sample_payload)
    end_time = time.perf_counter()

    total_time = end_time - start_time
    ops_per_sec = iterations / total_time
    print(f"\n--- BENCHMARK RESULTS ---")
    print(f"Total Iterations: {iterations:,}")
    print(f"Total Execution Time: {total_time:.4f} seconds")
    print(f"Throughput: {ops_per_sec:,.2f} ops/sec")
    return ops_per_sec

if __name__ == "__main__":
    run_benchmark()