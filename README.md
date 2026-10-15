# SkinRoll — Provably Fair Verifier

Public, self-contained verifier for SkinRoll rolls. **The verification runs entirely in your browser** (Web Crypto API) — no server, no tracking, no data sent anywhere.

## Use it

Open the GitHub Pages site of this repository and paste:

| Field | Where to find it |
|---|---|
| Client Seed | site → **MENU → Fairness Verification** |
| Server Seed | shown after you **rotate** the seed (seeds are hashed before use) |
| Secret Salt | revealed together with the server seed |
| Nonce | the bet's nonce (shown next to the roll) |

Optionally paste the **expected roll** to get a pass/fail check.

## Algorithm

```
Public Hash = HMAC_SHA256(key = secret_salt, message = server_seed)
Roll        = HMAC_SHA512(key = "<client_seed>-<nonce>", message = server_seed)
              → take the first 15 hex characters
              → parse as an integer (base 16)
              → modulo 100000
              → + 1        ⇒ 1 .. 100000
```

Nothing about the outcome depends on data the player cannot see before committing their client seed:
the server seed is hashed and published first, and can only be verified after it is revealed.

## Independent verification

* `index.html` — browser verifier (GitHub Pages)
* `verify.py` — same logic in Python, for offline/local checks:

```bash
python3 verify.py --client-seed <cs> --server-seed <ss> --nonce <n>
```

## Scope

This repository contains **only** the verifier. It is not part of the game code and has no access to any account data.

## 中文说明

本仓库是 SkinRoll 开奖结果的**公共验证器**，与站点业务代码完全独立。

- 全部计算在**你的浏览器本地完成**（Web Crypto），不联网、不上传任何数据
- 算法与站点后端（PHP `hash_hmac`）一致，并已用真实历史记录核对通过
- 校验公示 hash：`HMAC_SHA256(key = secret_salt, message = server_seed)`
- 计算 roll：`HMAC_SHA512(key = "<client_seed>-<nonce>", message = server_seed)` 取前 15 位十六进制 ⇒ 转为整数 ⇒ 对 100000 取模 ⇒ +1
- `verify.py` 提供等价的 Python 实现，便于本地/离线复核

## License

MIT
