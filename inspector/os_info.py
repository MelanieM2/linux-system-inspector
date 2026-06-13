import psutil
import platform
import os
import socket
from datetime import datetime, timezone


def get_os_info() -> dict:
    """Collect operating system information and return as a dictionary."""

    boot_time = psutil.boot_time() # Returns the system boot time as a Unix timestamp — a float representing the number of seconds elapsed since January 1st 1970 00:00:00 UTC
    uptime_seconds = datetime.now(timezone.utc).timestamp() - boot_time  # datetime.now(timezone.utc).timestamp() gets the current time as a Unix timestamp. 
                                                                         # Subtracting boot time gives elapsed seconds since boot — the uptime. 
                                                                         # We work in UTC internally and convert to local time only for display.

    hours, remainder = divmod(int(uptime_seconds), 3600)
    minutes, seconds = divmod(remainder, 60)

    return {
        "os": platform.system(),
        "os_version": platform.version(),
        "kernel": platform.release(),
        "hostname": socket.gethostname(),
        "username": os.getenv("USER") or os.getenv("USERNAME"),
        "uptime": f"{hours}h {minutes}m {seconds}s",
        "boot_time": datetime.fromtimestamp(
            boot_time, tz=timezone.utc
        ).strftime("%Y-%m-%d %H:%M:%S UTC"),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(get_os_info(), indent=2))