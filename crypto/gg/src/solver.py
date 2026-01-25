from hashlib import sha256
from binascii import unhexlify

# ===== Given =====
p = 170141183460469231731687303715884105727
g = 21573159886032097717357783100356254528
A = 53869325212687074329851985870878688230
B = 17670385730615880194037350268132002944
ciphertext = unhexlify("99ffc6a5ad572a466c86a202d54f26e73d089c873f348ce9")

# ===== Step 1: Solve discrete log in small subgroup =====
print("[*] Solving discrete log...")

a = None
MAX = 1 << 16   # 65536 (medium, intentional)

for i in range(MAX):
    if pow(g, i, p) == A:
        a = i
        print("[+] Found private key a =", a)
        break

if a is None:
    raise Exception("Private key not found — increase search range")

# ===== Step 2: Compute shared secret =====
s = pow(B, a, p)

# ===== Step 3: Derive key =====
key = sha256(str(s).encode()).digest()

# ===== Step 4: Decrypt =====
flag = bytes(c ^ k for c, k in zip(ciphertext, key))

print("[+] Flag:", flag)
