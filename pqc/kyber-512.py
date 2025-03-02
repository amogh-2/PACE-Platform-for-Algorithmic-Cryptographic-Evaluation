import time

from kyber_py.modules.modules import ModuleKyber

def benchmark_kyber(input_file="test.txt", output_file="kyber_benchmark.txt"):
    kyber = ModuleKyber()
    
    # Read test file data
    with open(input_file, "rb") as f:
        test_data = f.read()
    
    # Generate keypair
    start_time = time.time()
    keypair = kyber.generate_keypair()
    keygen_time = time.time() - start_time
    
    public_key, secret_key = keypair["pk"], keypair["sk"]
    
    # Key encapsulation
    start_time = time.time()
    ciphertext, shared_secret_enc = kyber.encapsulate(public_key)
    encapsulation_time = time.time() - start_time
    
    # Key decapsulation
    start_time = time.time()
    shared_secret_dec = kyber.decapsulate(ciphertext, secret_key)
    decapsulation_time = time.time() - start_time
    
    # Verify that the shared secret is correctly decapsulated
    success = shared_secret_enc == shared_secret_dec
    
    # Write results to a file
    with open(output_file, "w") as f:
        f.write(f"Test File Size: {len(test_data)} bytes\n")
        f.write(f"Key Generation Time: {keygen_time:.6f} seconds\n")
        f.write(f"Encapsulation Time: {encapsulation_time:.6f} seconds\n")
        f.write(f"Decapsulation Time: {decapsulation_time:.6f} seconds\n")
        f.write(f"Success: {success}\n")

    print("Benchmarking complete. Results saved to", output_file)

if __name__ == "__main__":
    benchmark_kyber("/home/amogh/Videos/test.txt")
