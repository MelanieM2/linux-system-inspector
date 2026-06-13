import psutil


def get_ram_info() -> dict:
    """Collect RAM and swap memory information and return as a dictionary."""

    ram = psutil.virtual_memory() # Returns a "named tuple" with fields describing the physical RAM
                                  # A named tuple is like a regular tuple (an ordered collection) 
                                  # but with named fields you can access with dot notation — so ram.total instead of ram[0]
    swap = psutil.swap_memory()

    return {
        "total_gb": round(ram.total / (1024**3), 2), # total physical RAM in bytes
        "used_gb": round(ram.used / (1024**3), 2), # RAM currently in use by processes
        "free_gb": round(ram.free / (1024**3), 2), # RAM not used at all
        "available_gb": round(ram.available / (1024**3), 2), #RAM available for new processes without swapping
        "usage_percent": ram.percent, # usage as a percentage, pre-calculated by psutil
        "swap_total_gb": round(swap.total / (1024**3), 2),
        "swap_used_gb": round(swap.used / (1024**3), 2),
        "swap_free_gb": round(swap.free / (1024**3), 2),
        "swap_usage_percent": swap.percent,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(get_ram_info(), indent=2))