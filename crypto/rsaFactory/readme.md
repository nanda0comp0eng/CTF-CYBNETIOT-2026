CHALLENGE DESCRIPTION:
A company deployed an in-house RSA key generator to mass-produce 
certificates. Two public keys were leaked, and the admin claims:

"Don't worry, they don't share primes. We already checked with gcd(n1, n2)."

Hmm, but something seems off about these keys...

HINT: The key generator reuses an internal secret value during prime 
generation. Sometimes the greatest common divisor reveals more than 
expected...
