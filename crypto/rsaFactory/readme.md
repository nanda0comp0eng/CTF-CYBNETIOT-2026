# rsaFactory

## Description

A company deployed an **in-house RSA key generator** to mass-produce digital certificates for internal services.  
Unfortunately, during a routine audit, **two RSA public keys were leaked**.

When confronted, the system administrator confidently stated:

> *"Don't worry, they don't share primes. We already checked with `gcd(n1, n2)`."*

At first glance, the claim seems valid, the moduli are coprime.  
However, cryptography is rarely that simple…

Something subtle went wrong during **prime generation**, and the relationship between the keys is far more dangerous than it appears.

Your mission is to analyze the leaked keys, uncover the hidden weakness, and recover the secret message.

## Hint

The key generator **reuses an internal secret value** during prime generation.  
Sometimes, the **greatest common divisor** reveals more than expected — even when it’s not obvious at first glance.

Flag: CYBNETIOT{4lg3br4ic_r3l4ti0ns_br34k_rs4_t00!}
