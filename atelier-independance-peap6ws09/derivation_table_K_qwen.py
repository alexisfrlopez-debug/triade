import math

def table_K():
    # Generate the first 64 prime numbers
    primes = [2]
    num = 3
    while len(primes) < 64:
        if all(num % p != 0 for p in primes):
            primes.append(num)
        num += 2
    
    # Compute the cube roots of the primes and take the fractional parts
    K = []
    for p in primes:
        cube_root = round(p ** (1/3), 32)
        fractional_part = cube_root - int(cube_root)
        K.append(int(fractional_part * (2**32)))
    
    return K

# Example usage
print(table_K())
