import psutil
import platform # part of Python's standard library


def get_cpu_info() -> dict:
    """Collect CPU information and return as a dictionary."""

    freq = psutil.cpu_freq() #Returns an object with three attributes: "current", "min", "max" — all in MHz.

    return {
        # platform.processor() returns the CPU model name as a string. It reads from the OS, not from psutil
        
        # TODO: replace platform.processor() with /proc/cpuinfo parsing
        # platform.processor() returns "x86_64" on Linux (architecture, not model name)
        # Fix during polish pass after all modules are complete
        "model": platform.processor(), 

        # my HP has 2 physical cores but 4 logical cores because of hyperthreading —each physical core presents itself to the OS as 2 virtual cores.
        "cores_physical": psutil.cpu_count(logical=False), # counts physical cores only (2)
        "cores_logical": psutil.cpu_count(logical=True), #  counts logical cores including hyperthreading (4)

        # Measuring the CPU usage as a percentage. The interval=1 argument means "measure over 1 second.  This is important: CPU usage is not a snapshot, it's a ratio of busy time to total time over an interval
        "usage_percent_overall": psutil.cpu_percent(interval=1), # Without percpu → returns one number for overall CPU usage
        "usage_percent_per_core": psutil.cpu_percent(interval=1, percpu=True), # with percpu = True, it returns a list, one percentage per logical core

        # On some systems (including some WSL2 configurations) this can return None, which is why we write:
        "freq_current_mhz": round(freq.current, 1) if freq else None,
        "freq_min_mhz": round(freq.min, 1) if freq and freq.min != 0.0 else None,
        "freq_max_mhz": round(freq.max, 1) if freq and freq.max != 0.0 else None,
    }

if __name__ == "__main__":
    import json
    print(json.dumps(get_cpu_info(), indent=2))