import numpy as np
from scipy.stats import ks_1samp, uniform

def lcg(modulus, a, c, seed, size):
    x = seed
    numbers = []
    for _ in range(size):
        x = (a * x + c) % modulus
        numbers.append(x / modulus)
    return np.array(numbers)

modulus = 2**31 - 1
a = 1103515245
c = 12345
seed = 42

size = 10000
lcg_numbers = lcg(modulus, a, c, seed, size)
mersenne_numbers = np.random.random(size) # Usando el Mersenne Twister predeterminado de NumPy

lcg_ks_stat, lcg_p_value = ks_1samp(lcg_numbers, uniform.cdf)
mersenne_ks_stat, mersenne_p_value = ks_1samp(mersenne_numbers, uniform.cdf)

print("LCG:")
print(f"Estadística KS: {lcg_ks_stat:.4f}, p-valor: {lcg_p_value:.4f}")

print("\nMersenne Twister:")
print(f"Estadística KS: {mersenne_ks_stat:.4f}, p-valor: {mersenne_p_value:.4f}")
