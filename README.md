# Linux System Inspector

A command-line tool that inspects a Linux system and produces structured reports on CPU, RAM, disk, network, and operating system information. Output is available in human-readable Markdown or machine-readable JSON.

Built as the first portfolio project in a structured transition toward AI/Data Science and ML engineering, this tool demonstrates professional Python packaging, defensive programming, CLI design, and supply chain security practices.

---

## What It Does

Running the tool produces a full system report:

```
## System Report — 2026-06-13 22:45:47 UTC

## CPU
- **Model:** x86_64
- **Physical cores:** 2
- **Logical cores:** 4
- **Usage (overall):** 2.7%
- **Usage (per core):** [3.0, 6.8, 7.8, 3.0]
- **Frequency (current):** 2592.0 MHz

## RAM
- **Total:** 7.7 GB
- **Used:** 1.91 GB
- **Available:** 5.79 GB
- **Usage:** 24.8%
- **Swap total:** 2.0 GB
- **Swap used:** 0.0 GB

## Disk
- **/**
  - Device: /dev/sdd
  - Filesystem: ext4
  - Total: 1006.85 GB
  - Used: 11.42 GB
  - Free: 944.21 GB
  - Usage: 1.2%

## Network
- **lo**
  - Address: 127.0.0.1 (family: 2)
  - Sent: 38.0 MB / Received: 38.0 MB
- **eth0**
  - Address: 172.23.213.96 (family: 2)
  - Sent: 2.38 MB / Received: 4.35 MB

## Operating System
- **OS:** Linux
- **Kernel:** 6.18.33.1-microsoft-standard-WSL2
- **Hostname:** your-hostname
- **Username:** your-username
- **Uptime:** 4h 10m 10s
- **Boot time:** 2026-06-13 17:28:06 UTC
```

---

## Installation

### Prerequisites

- Linux or WSL2 (Ubuntu)
- [uv](https://docs.astral.sh/uv/) — Python package manager

### Setup

```bash
git clone git@github.com:MelanieM2/linux-system-inspector.git
cd linux-system-inspector
uv sync
```

`uv sync` reads `pyproject.toml` and `uv.lock` and installs all dependencies into an isolated virtual environment automatically. No manual `pip install` or virtual environment activation is needed.

---

## Usage

### Full report (all modules, Markdown)

```bash
uv run main.py
```

### Select specific modules

```bash
uv run main.py --cpu
uv run main.py --ram
uv run main.py --disk
uv run main.py --network
uv run main.py --os
uv run main.py --ram --os
```

### Output formats

```bash
uv run main.py --format md      # Markdown (default)
uv run main.py --format json    # JSON
```

### Save report to file

```bash
uv run main.py --output report.md
uv run main.py --format json --output report.json
```

### Help

```bash
uv run main.py --help
```

---

## Running Tests

```bash
uv run pytest tests/ -v
```

All 15 tests cover invariants — properties that must hold on any valid Linux system — rather than machine-specific values, making the test suite portable across different hardware.

---

## Project Structure

```
linux-system-inspector/
├── inspector/
│   ├── __init__.py
│   ├── cpu.py          — CPU model, cores, usage, frequency
│   ├── ram.py          — physical RAM and swap memory
│   ├── disk.py         — partitions, usage per mountpoint
│   ├── network.py      — interfaces, addresses, I/O counters
│   └── os_info.py      — OS, kernel, hostname, uptime
├── tests/
│   ├── __init__.py
│   ├── test_cpu.py     — 7 tests
│   └── test_ram.py     — 8 tests
├── main.py             — CLI entry point (argparse)
├── reporter.py         — Markdown and JSON formatting
├── pyproject.toml      — project config and dependencies
├── uv.lock             — cryptographic dependency lockfile
└── SECURITY.md         — supply chain security documentation
```

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.12 | Language |
| psutil | System metrics collection |
| argparse | CLI interface |
| pathlib | File output handling |
| platform / socket / os | OS and network metadata |
| pytest | Unit testing |
| uv | Package management and virtual environments |

---

## Security

We apply supply chain security practices to all dependencies. See [SECURITY.md](SECURITY.md) for full documentation covering exact version pinning, quarantine buffering, vulnerability scanning with `uv audit`, and cryptographic lockfile verification.

---

## Known Limitations

- `platform.processor()` returns the architecture string (`x86_64`) on Linux rather than the CPU model name. A fix using `/proc/cpuinfo` is planned for a future polish pass.
- On WSL2, `freq_min_mhz` and `freq_max_mhz` are unavailable and reported as `null`. Only the current frequency is accessible.
- Disk output on WSL2 shows the virtual disk (`/dev/sdd`) across multiple mountpoints with identical usage figures, reflecting WSL2's single `.vhdx` virtual disk architecture.

---

## Roadmap

- [ ] Replace `platform.processor()` with `/proc/cpuinfo` parsing for accurate CPU model names
- [ ] Deduplicate disk partitions by device
- [ ] Add `--remote` flag for SSH-based inspection of remote machines
- [ ] Mock `cpu_percent(interval=1)` in tests to reduce suite runtime
- [ ] Add Windows drive visibility via `disk_partitions(all=True)`

---

## Development Notes

Developed through guided learning sessions using **Claude Sonnet 4.6** 
(Anthropic) as an AI pair-programming assistant used via chat interface. This was used to explain and learn
concepts, review code structure, and discuss design decisions. 
All modules were written, tested, and validated by the author, 
with a focus on deep understanding over code generation.

## Author

Melanie Maldonado is a professional Mathematician (Differential Geometry and Mathematical Physics), transitioning to AI/Data Science/ML Engineering.

This project is part of a series designed to help her learn more about Linux, Bash scripting, AI engineering, data science, machine learning, and geometric deep learning.
