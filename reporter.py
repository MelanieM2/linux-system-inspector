import json
from datetime import datetime, timezone


def generate_report(data: dict, fmt: str = "md") -> str:
    """Format collected system data as Markdown or JSON string.
    
    Args:
        data: dictionary containing all inspector module outputs
        fmt:  output format — "md" for Markdown, "json" for JSON
    
    Returns:
        formatted report as a string
    """

    if fmt == "json":
        return _format_json(data)
    else:
        return _format_markdown(data)


def _format_json(data: dict) -> str:
    """Return pretty-printed JSON string."""
    return json.dumps(data, indent=2)


def _format_markdown(data: dict) -> str:
    """Return formatted Markdown report string."""

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    lines = []

    lines.append(f"# System Report — {timestamp}")
    lines.append("")

    # CPU section
    if "cpu" in data:
        cpu = data["cpu"]
        lines.append("## CPU")
        lines.append(f"- **Model:** {cpu.get('model', 'N/A')}")
        lines.append(f"- **Physical cores:** {cpu.get('cores_physical', 'N/A')}")
        lines.append(f"- **Logical cores:** {cpu.get('cores_logical', 'N/A')}")
        lines.append(f"- **Usage (overall):** {cpu.get('usage_percent_overall', 'N/A')}%")
        lines.append(f"- **Usage (per core):** {cpu.get('usage_percent_per_core', 'N/A')}")
        lines.append(f"- **Frequency (current):** {cpu.get('freq_current_mhz', 'N/A')} MHz")
        lines.append("")

    # RAM section
    if "ram" in data:
        ram = data["ram"]
        lines.append("## RAM")
        lines.append(f"- **Total:** {ram.get('total_gb', 'N/A')} GB")
        lines.append(f"- **Used:** {ram.get('used_gb', 'N/A')} GB")
        lines.append(f"- **Available:** {ram.get('available_gb', 'N/A')} GB")
        lines.append(f"- **Usage:** {ram.get('usage_percent', 'N/A')}%")
        lines.append(f"- **Swap total:** {ram.get('swap_total_gb', 'N/A')} GB")
        lines.append(f"- **Swap used:** {ram.get('swap_used_gb', 'N/A')} GB")
        lines.append("")

    # Disk section
    if "disk" in data:
        lines.append("## Disk")
        for partition in data["disk"].get("partitions", []):
            if "error" in partition:
                lines.append(f"- **{partition['mountpoint']}:** permission denied")
            else:
                lines.append(f"- **{partition['mountpoint']}**")
                lines.append(f"  - Device: {partition.get('device', 'N/A')}")
                lines.append(f"  - Filesystem: {partition.get('filesystem', 'N/A')}")
                lines.append(f"  - Total: {partition.get('total_gb', 'N/A')} GB")
                lines.append(f"  - Used: {partition.get('used_gb', 'N/A')} GB")
                lines.append(f"  - Free: {partition.get('free_gb', 'N/A')} GB")
                lines.append(f"  - Usage: {partition.get('usage_percent', 'N/A')}%")
        lines.append("")

    # Network section
    if "network" in data:
        lines.append("## Network")
        for interface in data["network"].get("interfaces", []):
            lines.append(f"- **{interface['name']}**")
            for addr in interface.get("addresses", []):
                lines.append(f"  - Address: {addr.get('address', 'N/A')} (family: {addr.get('family', 'N/A')})")
            lines.append(f"  - Sent: {interface.get('bytes_sent_mb', 'N/A')} MB")
            lines.append(f"  - Received: {interface.get('bytes_recv_mb', 'N/A')} MB")
        lines.append("")

    # OS section
    if "os" in data:
        os_info = data["os"]
        lines.append("## Operating System")
        lines.append(f"- **OS:** {os_info.get('os', 'N/A')}")
        lines.append(f"- **Kernel:** {os_info.get('kernel', 'N/A')}")
        lines.append(f"- **Hostname:** {os_info.get('hostname', 'N/A')}")
        lines.append(f"- **Username:** {os_info.get('username', 'N/A')}")
        lines.append(f"- **Uptime:** {os_info.get('uptime', 'N/A')}")
        lines.append(f"- **Boot time:** {os_info.get('boot_time', 'N/A')}")
        lines.append("")

    return "\n".join(lines)


