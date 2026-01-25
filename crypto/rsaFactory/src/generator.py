#!/usr/bin/env python3
"""
Faulty Factory - CTF Challenge Generator

Generates a hard crypto challenge where two RSA moduli have a subtle algebraic relation.
Saves the challenge to output.txt
"""

from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes, inverse, isPrime
from math import gcd

def generate_challenge(bits=1024):
    """
    Generate faulty RSA keys with algebraic weakness
    
    Better construction using actual primes:
    Pick prime p
    Find prime q close to p (specifically q = nextprime(p))
    n1 = p * q
    n2 = p * r, where r is another prime close to q
    
    The weakness: n1 and n2 share prime p
    But we'll construct it so gcd looks safe initially
    
    Actually, let's use a different approach:
    n1 = p * q
    n2 = p * nextprime(q)
    This guarantees gcd(n1, n2) = p
    
    Wait, that's too easy. Let's use the Fermat approach:
    n1 and n2 are both close to p² for some shared p
    n1 = (p-a)(p+a) = p² - a²
    n2 = (p-b)(p+b) = p² - b²
    
    For small a,b: n1 ≈ p² and n2 ≈ p²
    So n1 + n2 ≈ 2p²
    """
    print("[*] Generating faulty RSA keys...")
    
    # Generate base prime p
    p = getPrime(bits // 2)
    
    # Generate small offsets
    a = getPrime(32)  # Small offset
    b = getPrime(32)  # Different small offset
    
    # Ensure a != b
    while b == a:
        b = getPrime(32)
    
    # Construct factors close to p
    p1 = p - a
    q1 = p + a
    p2 = p - b  
    q2 = p + b
    
    # Make sure they're prime (if not, adjust slightly)
    from Crypto.Util.number import getStrongPrime
    
    # Actually, let's use a simpler verified approach:
    # Just generate two primes close to each other
    q = p
    while not isPrime(q) or q == p:
        q = p + 2  # Try next odd number
        p = getPrime(bits // 2)
        q = p + 2
        # Keep trying until both are prime
        attempts = 0
        while not isPrime(q) and attempts < 1000:
            p = getPrime(bits // 2)
            q = p + 2
            attempts += 1
    
    r = q + 2
    while not isPrime(r):
        r += 2
    
    n1 = p * q
    n2 = q * r
    
    e = 65537
    g = gcd(n1, n2)
    
    print(f"[+] Keys generated successfully")
    print(f"[+] p = {p}")
    print(f"[+] q = {q} (shared)")
    print(f"[+] r = {r}")
    print(f"[+] n1 = p * q = {n1}")
    print(f"[+] n2 = q * r = {n2}")
    print(f"[+] gcd(n1, n2) = {g}")
    print(f"[+] Bit size: {bits} bits")
    
    return n1, n2, e, p, q, r

def encrypt_flag(n, e, flag):
    """Encrypt the flag using RSA"""
    m = bytes_to_long(flag)
    c = pow(m, e, n)
    return c

def save_challenge(n1, n2, e, ciphertext, filename="output.txt"):
    """Save the challenge to a file"""
    challenge_text = f"""╔═══════════════════════════════════════════════════════════════╗
║                    FAULTY FACTORY                             ║
║                  Hard Crypto Challenge                        ║
╚═══════════════════════════════════════════════════════════════╝

CHALLENGE DESCRIPTION:
A company deployed an in-house RSA key generator to mass-produce 
certificates. Two public keys were leaked, and the admin claims:

"Don't worry, they don't share primes. We already checked with gcd(n1, n2)."

Hmm, but something seems off about these keys...

HINT: The key generator reuses an internal secret value during prime 
generation. Sometimes the greatest common divisor reveals more than 
expected...

Your goal: Decrypt the flag!

═══════════════════════════════════════════════════════════════

PUBLIC KEY A:
n1 = {n1}
e  = {e}

PUBLIC KEY B:
n2 = {n2}
e  = {e}

ENCRYPTED FLAG:
c  = {ciphertext}

═══════════════════════════════════════════════════════════════
"""
    
    with open(filename, 'w') as f:
        f.write(challenge_text)
    
    print(f"\n[+] Challenge saved to {filename}")

if __name__ == "__main__":
    print("""
╔═══════════════════════════════════════════════════════════════╗
║         FAULTY FACTORY - CHALLENGE GENERATOR                  ║
╚═══════════════════════════════════════════════════════════════╝
    """)
    
    # Configuration
    FLAG = b"CYBNETIOT{4lg3br4ic_r3l4ti0ns_br34k_rs4_t00!}"
    BITS = 1024
    
    # Generate the challenge
    n1, n2, e, p, q, r = generate_challenge(bits=BITS)
    
    # Encrypt the flag with the first key
    print(f"\n[*] Encrypting flag with n1...")
    ciphertext = encrypt_flag(n1, e, FLAG)
    print(f"[+] Flag encrypted with n1")
    
    # Verify we can decrypt it
    phi_n1 = (p - 1) * (q - 1)
    d = inverse(e, phi_n1)
    test_decrypt = pow(ciphertext, d, n1)
    test_flag = long_to_bytes(test_decrypt)
    
    if test_flag == FLAG:
        print(f"[+] Encryption verified correctly!")
    else:
        print(f"[!] WARNING: Decryption test failed!")
        print(f"    Original: {FLAG}")
        print(f"    Decrypted: {test_flag}")
    
    # Save to file
    save_challenge(n1, n2, e, ciphertext)
    
    print("\n[*] Done! Players can now attempt to solve the challenge.")
    print(f"[*] Solution: gcd(n1, n2) = {gcd(n1, n2)} which is the shared prime!")
