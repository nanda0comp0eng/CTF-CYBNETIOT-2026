#!/usr/bin/env python3
"""
Faulty Factory - CTF Challenge Solver

Exploits shared prime between two RSA moduli.
"""

from Crypto.Util.number import long_to_bytes, inverse
from math import gcd

def solve():
    """
    Solve the Faulty Factory challenge
    
    The weakness: n1 and n2 share a common prime factor
    n1 = p * q
    n2 = p * r
    
    Therefore: gcd(n1, n2) = p (the shared prime)
    """
    
    # Challenge data
    n1 = 64526263057392838201923618034898385508386355084143630852729486007405244114355800959446187337907450977148904551332004513023847376375521548013715568808421773252331372669487336267760051006453527683539016954914889559721083641051557566050605502576127648001766791737277268476864120413033224482879407332769982385283
    n2 = 64526263057392838201923618034898385508386355084143630852729486007405244114355800959446187337907450977148904551332004513023847376375521548013715568808429934601619239970513391020854974907136994015283516222086972509359351936777253964626131509239679639466977883573285150135162182717613794223583688047234402256747
    e = 65537
    c = 3163198831077821633373344333313349970176100504121709912530067428083632047047719946677544258295551211855368677833337869516747632852097074090797373608928854803492626164264484164850605034029290993766297475384765351033510276951251135042583743937058015416652012862467052049120961415395718997052667850494443470647
    
    print("╔═══════════════════════════════════════════════════════════════╗")
    print("║              FAULTY FACTORY - SOLVER                          ║")
    print("╚═══════════════════════════════════════════════════════════════╝\n")
    
    # Step 1: Compute GCD
    print("[*] Step 1: Computing gcd(n1, n2)...")
    print("    The hint says: 'Sometimes a large GCD is more dangerous than gcd=1'")
    print("    Let's see what we get...\n")
    
    shared_prime = gcd(n1, n2)
    
    if shared_prime == 1:
        print("    [-] gcd = 1, no shared prime found")
        print("    [!] This challenge may use a different approach")
        return
    elif shared_prime == n1 or shared_prime == n2:
        print("    [-] gcd equals one of the moduli, something's wrong")
        return
    else:
        print(f"    [+] GCD = {shared_prime}")
        print(f"    [+] This is a LARGE number - it must be the shared prime!")
        print(f"    [+] Got it! This is the vulnerability!\n")
    
    # Step 2: Factor both moduli
    print("[*] Step 2: Using the shared prime to factor both moduli...")
    
    p = shared_prime
    q = n1 // p
    r = n2 // p
    
    print(f"    [+] n1 = p × q")
    print(f"        where p = {p}")
    print(f"        and   q = {q}")
    print(f"    [+] n2 = p × r") 
    print(f"        where r = {r}\n")
    
    # Verify factorization
    if p * q != n1:
        print("    [!] ERROR: Factorization of n1 failed!")
        return
    if p * r != n2:
        print("    [!] ERROR: Factorization of n2 failed!")
        return
    
    print("    [+] Factorization verified!\n")
    
    # Step 3: Compute private exponent for n1
    print("[*] Step 3: Computing private key for n1...")
    print(f"    φ(n1) = (p-1) × (q-1)")
    phi_n1 = (p - 1) * (q - 1)
    
    print(f"    Computing d ≡ e^(-1) mod φ(n1)...")
    d = inverse(e, phi_n1)
    print(f"    [+] Private exponent d computed!\n")
    
    # Step 4: Decrypt
    print("[*] Step 4: Decrypting the ciphertext...")
    print(f"    m = c^d mod n1")
    m = pow(c, d, n1)
    flag = long_to_bytes(m)
    
    print("\n╔═══════════════════════════════════════════════════════════════╗")
    print("║                         FLAG FOUND!                           ║")
    print("╚═══════════════════════════════════════════════════════════════╝\n")
    
    try:
        flag_str = flag.decode('utf-8')
        print(f"    {flag_str}\n")
    except:
        print(f"    Raw bytes: {flag}")
        print(f"    Hex: {flag.hex()}\n")
    
    # Verification
    print("═" * 67)
    print("ATTACK SUMMARY")
    print("═" * 67)
    print(f"Vulnerability: Shared prime between n1 and n2")
    print(f"Attack method: Compute gcd(n1, n2) to recover shared prime")
    print(f"Shared prime p = {p}")
    print(f"n1 factored: ✓")
    print(f"n2 factored: ✓")
    print(f"Flag decrypted: ✓")
    print("═" * 67)
    print("\nLesson: NEVER reuse primes across different RSA keys!")
    print("Each RSA key pair must use completely unique primes.")

if __name__ == "__main__":
    solve()
