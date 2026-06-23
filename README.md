# Linux System Inspector

In this project, we build a command-line system inspection tool that collects and reports structured information about CPU, memory, disk, network, and operating system state.

The tool is designed as a portable systems diagnostics utility with both human-readable (Markdown) and machine-readable (JSON) output formats. It emphasizes reproducibility, modular design, and invariant-based testing rather than machine-specific assumptions.

This project is part of a broader systems engineering progression focused on Linux infrastructure, automation, and AI-assisted tooling.

---

## What It Does

The tool generates a complete snapshot of the system state:

* CPU usage, cores, frequency
* RAM and swap utilization
* Disk partitions and storage usage
* Network interfaces and traffic statistics
* Operating system metadata (kernel, uptime, host info)

Output can be generated in:

* Markdown (human-readable reports)
* JSON (machine-readable structured data)

---

## Key Design Goals

* Provide a unified CLI for system introspection
* Ensure portability across Linux and WSL2 environments
* Separate data collection from presentation logic
* Support both human and machine consumption formats
* Validate system behavior using invariant-based testing

---

## Installation

### Prerequisites

* Linux or WSL2 (Ubuntu recommended)
* Python 3.12+
* uv (modern Python environment manager)

### Setup

```bash id="q9k2l1"
git clone git@github.com:your-username/linux-system-inspector.git
cd linux-system-inspector
uv sync
```

Dependencies are installed into an isolated environment managed by `uv`, removing the need for manual virtual environment activation.

---

## Usage

### Full system report

```bash id="k2v9x3"
uv run main.py
```

### Select specific modules

```bash id="m8p1q7"
uv run main.py --cpu
uv run main.py --ram
uv run main.py --disk
uv run main.py --network
uv run main.py --os
```

### Output formats

```bash id="t5n0z2"
uv run main.py --format md
uv run main.py --format json
```

### Save output to file

```bash id="r3v8a1"
uv run main.py --output report.md
uv run main.py --format json --output report.json
```

---

## Project Structure

```text id="p1x7d9"
linux-system-inspector/
├── inspector/
│   ├── cpu.py
│   ├── ram.py
│   ├── disk.py
│   ├── network.py
│   └── os_info.py
├── tests/
│   ├── test_cpu.py
│   └── test_ram.py
├── main.py
├── reporter.py
├── pyproject.toml
├── uv.lock
└── SECURITY.md
```

---

## Architecture

The system follows a modular separation of concerns:

* **Inspector modules** → collect raw system data
* **Reporter layer** → formats data into Markdown or JSON
* **CLI layer** → parses arguments and orchestrates execution
* **Test layer** → validates system invariants across environments

This separation allows the tool to remain extensible while keeping data collection logic independent from output formatting.

---

## Testing Philosophy

The test suite is built around **system invariants rather than fixed values**.

Instead of asserting machine-specific outputs, tests verify properties such as:

* CPU core count is positive
* RAM usage percentages are within valid bounds
* Disk usage values are consistent and non-negative
* Network counters increase monotonically over time

This approach ensures portability across:

* different hardware configurations
* virtual machines
* WSL2 environments

---

## Tech Stack

| Component      | Technology  |
| -------------- | ----------- |
| Language       | Python 3.12 |
| System Metrics | psutil      |
| CLI            | argparse    |
| Filesystem     | pathlib     |
| Networking     | socket      |
| Testing        | pytest      |
| Environment    | uv          |

---

## Security & Supply Chain Practices

This project follows strict dependency and supply chain security principles:

* Fully pinned dependencies via `uv.lock`
* Reproducible environment resolution with `uv`
* Isolated virtual environments per project
* Explicit dependency declarations in `pyproject.toml`
* No runtime network dependency for core functionality

See `SECURITY.md` for detailed security methodology.

---

## Known Limitations

* CPU model detection relies on `platform.processor()`, which may return architecture strings instead of full CPU names on Linux.
* WSL2 does not expose full frequency range metadata (`freq_min`, `freq_max`).
* Disk reporting reflects WSL2 virtual disk architecture, which may aggregate mountpoints under a single virtual device.

---

## Roadmap

* Improve CPU detection via `/proc/cpuinfo`
* Deduplicate disk mount reporting for WSL2 environments
* Add SSH-based remote inspection mode (`--remote`)
* Improve test performance by mocking CPU load sampling
* Extend compatibility for Windows-native disk reporting

---


## Development Notes & AI Usage

### AI-Assisted Pair-Programming

This repository is the result of an independent learning and development workflow, not agentic automation. While Claude Sonnet 4.6 was used to:

* generate structural snippets,
* clarify unfamiliar concepts,
* explore architectural design options,
* review and iterate on code structure,
* accelerate development of boilerplate and automation logic,

its output was above all used as a learning foundation. I evaluated, corrected, and manually typed the implementation to ensure a personal understanding of system design principles in Linux and Python.

---

## Project Context

This project is part of a broader personal engineering track focused on:

* Python-based automation systems
* Linux system architecture and infrastructure design
* Bash scripting for workflow automation
* Applied machine learning and LLM-integrated pipelines

The author's long-term goal is to develop her expertise at the intersection of mathematics, data science, artificial intelligence, and systems engineering, bridging mathematical foundations in machine learning and deep learning with practical experience in software development, automation, and production-grade infrastructure.

## Feedback

This project is part of an ongoing learning and engineering journey. Constructive feedback, corrections, and suggestions for improvement are greatly appreciated. Please feel free to open an issue or contact the author through GitHub.