#!/usr/bin/env python3
"""SkinRoll provably fair roll verifier (reference implementation).

Algorithm (identical to the site backend, PHP hash_hmac):

    Public Hash = HMAC_SHA256(key = secret_salt, message = server_seed)
    Roll        = HMAC_SHA512(key = "<client_seed>-<nonce>", message = server_seed)
                  first 15 hex chars -> int(., 16) -> modulus 100000 -> + 1

Usage:
    python3 verify.py --client-seed CS --server-seed SS --nonce N
    python3 verify.py --client-seed CS --server-seed SS --nonce N --expect 88545
    python3 verify.py --client-seed CS --server-seed SS --nonce N \
                      --secret-salt SALT --expect-hash <published hash>
"""
import argparse
import hashlib
import hmac


def public_hash(server_seed: str, secret_salt: str) -> str:
    return hmac.new(secret_salt.encode(), server_seed.encode(), hashlib.sha256).hexdigest()


def roll(server_seed: str, client_seed: str, nonce: int) -> int:
    key = f"{client_seed}-{nonce}".encode()
    digest = hmac.new(key, server_seed.encode(), hashlib.sha512).hexdigest()
    return int(digest[:15], 16) % 100000 + 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Verify a SkinRoll roll")
    ap.add_argument("--client-seed", required=True)
    ap.add_argument("--server-seed", required=True)
    ap.add_argument("--nonce", required=True, type=int)
    ap.add_argument("--expect", type=int, help="roll reported by the site")
    ap.add_argument("--secret-salt", help="to also verify the published hash")
    ap.add_argument("--expect-hash", help="published hash to compare against")
    a = ap.parse_args()

    r = roll(a.server_seed, a.client_seed, a.nonce)
    print(f"roll          = {r}")
    if a.expect is not None:
        print(f"expected      = {a.expect}")
        print(f"result        = {'MATCH' if r == a.expect else 'MISMATCH'}")

    if a.secret_salt:
        h = public_hash(a.server_seed, a.secret_salt)
        print(f"public hash   = {h}")
        if a.expect_hash:
            ok = hmac.compare_digest(h.lower(), a.expect_hash.strip().lower())
            print(f"hash check    = {'MATCH' if ok else 'MISMATCH'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
