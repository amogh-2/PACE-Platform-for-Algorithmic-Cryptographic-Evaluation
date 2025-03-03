import time
import statistics
import argparse
from kyber_py.kyber.kyber import Kyber

def benchmark_kyber(parameter_set, iterations=100):
    kyber = Kyber(parameter_set=parameter_set)
    
    key_gen_times = []
    encap_times = []
    decap_times = []
    
    for _ in range(iterations):
        # Benchmark key generation
        start_time = time.time()
        public_key, secret_key = kyber.keygen()
        key_gen_times.append((time.time() - start_time) * 1000)  # Convert to milliseconds
        
        # Benchmark encapsulation
        start_time = time.time()
        shared_secret, encrypted_key = kyber.encaps(public_key)
        encap_times.append((time.time() - start_time) * 1000)  # Convert to milliseconds
        
        # Benchmark decapsulation
        start_time = time.time()
        decapsulated_secret = kyber.decaps(secret_key, encrypted_key)
        decap_times.append((time.time() - start_time) * 1000)  # Convert to milliseconds
        
        # Verify correctness (optional, but good for ensuring the operations work correctly)
        assert shared_secret == decapsulated_secret, "Decapsulation failed to recover the correct shared secret"

    return key_gen_times, encap_times, decap_times

def print_stats(operation, times):
    print(f"{operation} Statistics:")
    print(f"  Mean: {statistics.mean(times):.2f} ms")
    print(f"  Median: {statistics.median(times):.2f} ms")
    print(f"  Std Dev: {statistics.stdev(times):.2f} ms")
    print(f"  Min: {min(times):.2f} ms")
    print(f"  Max: {max(times):.2f} ms")
    print()

def main():
    parser = argparse.ArgumentParser(description="Benchmark Kyber Crystal operations")
    parser.add_argument("--security", type=int, choices=[1, 2, 3], default=3,
                        help="Security level (1=Kyber512, 2=Kyber768, 3=Kyber1024)")
    parser.add_argument("--iterations", type=int, default=100,
                        help="Number of iterations for each operation")
    args = parser.parse_args()

    security_params = {
        1: {"k": 2, "eta_1": 3, "eta_2": 2, "du": 10, "dv": 4},  # Kyber512
        2: {"k": 3, "eta_1": 2, "eta_2": 2, "du": 10, "dv": 4},  # Kyber768
        3: {"k": 4, "eta_1": 2, "eta_2": 2, "du": 11, "dv": 5}   # Kyber1024
    }

    print(f"Benchmarking Kyber Crystal (Security Level: {args.security})")
    print(f"Running {args.iterations} iterations for each operation")
    print()

    key_gen_times, encap_times, decap_times = benchmark_kyber(security_params[args.security], args.iterations)

    print_stats("Key Generation", key_gen_times)
    print_stats("Encapsulation", encap_times)
    print_stats("Decapsulation", decap_times)

if __name__ == "__main__":
    main()

