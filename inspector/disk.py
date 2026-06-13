import psutil


def get_disk_info() -> dict:
    """Collect disk partition and usage information and return as a dictionary."""

    partitions = []

    # TODO: consider psutil.disk_partitions(all=True) to include Windows drives (/mnt/c etc.)
    # TODO: consider deduplicating partitions by device to avoid redundant entries

    for partition in psutil.disk_partitions(): # Returns a list of all mounted partitions on the system. Each partition is a "named tuple" with fields:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            partitions.append({
                "device": partition.device,  # the device file, e.g. /dev/sdb or C:\ on Windows
                "mountpoint": partition.mountpoint, # where it's mounted in the filesystem, e.g. / or /mnt/c
                "filesystem": partition.fstype, # filesystem type, e.g. ext4, ntfs, tmpfs
                "total_gb": round(usage.total / (1024**3), 2),
                "used_gb": round(usage.used / (1024**3), 2),
                "free_gb": round(usage.free / (1024**3), 2),
                "usage_percent": usage.percent,
            })
        except PermissionError:
            partitions.append({
                "device": partition.device,
                "mountpoint": partition.mountpoint,
                "filesystem": partition.fstype,
                "error": "permission denied",
            })

    return {"partitions": partitions} # The final result is a list of dictionaries —one dictionary per partition
                                      # We wrap the list in a dictionary with a key, rather than just a bare list [...]
                                      # This keeps the return type consistent across all modules 


if __name__ == "__main__":
    import json
    print(json.dumps(get_disk_info(), indent=2))