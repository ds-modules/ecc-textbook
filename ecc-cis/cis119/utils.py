"""Utility functions for interactive RSA teaching demos.

These helpers are intentionally small and readable for classroom use.
Do not use these toy parameters for real-world security.
"""

from math import gcd


def egcd(a: int, b: int):
    """Extended Euclidean algorithm.

    Returns (g, x, y) such that a*x + b*y = g = gcd(a, b).
    """
    if a == 0:
        return b, 0, 1
    g, y, x = egcd(b % a, a)
    return g, x - (b // a) * y, y


def mod_inverse(a: int, m: int) -> int:
    """Return modular inverse of a mod m."""
    g, x, _ = egcd(a, m)
    if g != 1:
        raise ValueError('Inverse does not exist.')
    return x % m


def mod_inverse_trace(a: int, m: int):
    """Return modular inverse and a readable trace of EEA steps."""
    old_r, r = a, m
    old_s, s = 1, 0
    old_t, t = 0, 1
    rows = []

    while r != 0:
        q = old_r // r
        rows.append(
            {
                "q": q,
                "old_r": old_r,
                "r": r,
                "old_s": old_s,
                "s": s,
                "old_t": old_t,
                "t": t,
            }
        )
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t

    if old_r != 1:
        raise ValueError("Inverse does not exist.")
    return old_s % m, rows


def generate_toy_rsa(p: int = 61, q: int = 53, e: int = 17) -> dict:
    """Generate a toy RSA parameter set for demonstration."""
    n = p * q
    phi_n = (p - 1) * (q - 1)
    if gcd(e, phi_n) != 1:
        raise ValueError('e must be coprime with phi(n).')
    d = mod_inverse(e, phi_n)
    return {
        'p': p,
        'q': q,
        'n': n,
        'phi_n': phi_n,
        'e': e,
        'd': d,
        'public_key': (e, n),
        'private_key': (d, n),
    }


def rsa_encrypt(m: int, e: int, n: int) -> int:
    """Encrypt integer message m with public key (e, n)."""
    if not (0 <= m < n):
        raise ValueError('Message must satisfy 0 <= m < n.')
    return pow(m, e, n)


def rsa_decrypt(c: int, d: int, n: int) -> int:
    """Decrypt integer ciphertext c with private key (d, n)."""
    return pow(c, d, n)


def modular_pow_trace(base: int, exponent: int, modulus: int):
    """Trace square-and-multiply modular exponentiation steps."""
    result = 1
    b = base % modulus
    e = exponent
    step = 0
    rows = []

    while e > 0:
        bit = e & 1
        before_result = result
        if bit == 1:
            result = (result * b) % modulus
        rows.append(
            {
                "step": step,
                "bit": bit,
                "exp_before_shift": e,
                "base_value": b,
                "result_before": before_result,
                "result_after_maybe_multiply": result,
            }
        )
        b = (b * b) % modulus
        e >>= 1
        step += 1

    return rows, result


def rsa_steps(m: int, p: int = 61, q: int = 53, e: int = 17) -> dict:
    """Return all intermediate values for step-by-step RSA teaching."""
    params = generate_toy_rsa(p=p, q=q, e=e)
    d_check, inverse_rows = mod_inverse_trace(params["e"], params["phi_n"])
    encrypt_rows, c = modular_pow_trace(m, params["e"], params["n"])
    decrypt_rows, recovered = modular_pow_trace(c, params["d"], params["n"])
    return {
        **params,
        "inverse_rows": inverse_rows,
        "d_check": d_check,
        "message": m,
        "encrypt_rows": encrypt_rows,
        "ciphertext": c,
        "decrypt_rows": decrypt_rows,
        "recovered": recovered,
    }
