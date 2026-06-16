# Security Policy

This document describes the supply chain security framework applied to the `linux-system-inspector` project. Although this project served as a learning background for the author as solo project, these practices mitigate risks from dependency confusion attacks, malicious package releases, and silent background upgrades.

---

## 1. Dependency Pinning (`pyproject.toml`)

All dependencies are pinned to exact versions using a strict `uv` configuration:

```toml
[tool.uv]
add-bounds = "exact"
exclude-newer = "7 days ago"
```

### What these rules do

**`add-bounds = "exact"`** — forces `uv` to write dependencies using strict `==` version pinning instead of loose `>=` ranges. This means no dependency can silently upgrade to a newer version without an explicit manual decision.

**`exclude-newer = "7 days ago"`** — instructs `uv` to ignore any package release published within the last 7 days. This creates a quarantine buffer that significantly reduces exposure to newly injected malicious releases during their initial distribution window, before the community has had time to detect and report them.

---

## 2. Dependencies

### Production

| Package | Version | Notes |
|---|---|---|
| psutil | ==7.2.2 | Retrofitted from loose `>=7.2.2` to strict pinning |

### Development

| Package | Version | Notes |
|---|---|---|
| pytest | ==9.0.3 | Installed with `uv add --dev` — isolated from production environment |

All versions were verified to predate the 7-day quarantine threshold before being written to the lockfile.

---

## 3. Vulnerability Scanning

Before running any application code or the test suite, all dependencies were scanned against the Python Packaging Advisory Database:

```bash
uv audit
```

**Result:** `Found no known vulnerabilities and no adverse project statuses`

We run `uv audit` whenever dependencies are added or updated, and recommend doing the same after any `uv sync` on a fresh clone.

---

## 4. Cryptographic Lockfile

`uv.lock` is committed to version control. This file contains:

- Exact versions of all direct and transitive dependencies
- Cryptographic checksums (hashes) for every package

When running `uv sync` on a fresh clone, `uv` verifies every downloaded package against these checksums before installation. Any tampered or substituted package will fail verification and be rejected.

This means the environment is fully reproducible and cryptographically verified on every machine that clones the repository.

---

## 5. Safe Execution Rules

Always run code and tests inside the isolated project environment:

```bash
uv run main.py
uv run pytest tests/ -v
```

Never use a global `python` or `pip` invocation — this bypasses the virtual environment and the pinned dependency versions.

To clear the local package cache entirely:

```bash
uv cache clean
```

---

## 6. Reporting a Vulnerability

If you discover a security issue in this project, please open a GitHub issue with the label `security`. For sensitive disclosures, contact the author directly via GitHub.
