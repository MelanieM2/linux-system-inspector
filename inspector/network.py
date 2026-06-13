import psutil


def get_network_info() -> dict:
    """Collect network interface and I/O information and return as a dictionary."""

    interfaces = []
    io_counters = psutil.net_io_counters(pernic=True)  # pernic stands for per network interface card. 
                                                       # Without this flag, psutil returns one combined total across all interfaces. 
                                                       # With pernic=True it returns a dictionary keyed by interface name, 
                                                       # so we can look up I/O stats for each interface individually.

    for interface_name, addresses in psutil.net_if_addrs().items():

        interface_addresses = []
        for address in addresses:
            interface_addresses.append({
                "family": str(address.family),
                "address": address.address,
                "netmask": address.netmask,
            })

        io = io_counters.get(interface_name)
        interfaces.append({
            "name": interface_name,
            "addresses": interface_addresses,
            "bytes_sent_mb": round(io.bytes_sent / (1024**2), 2) if io else None,
            "bytes_recv_mb": round(io.bytes_recv / (1024**2), 2) if io else None,
            "packets_sent": io.packets_sent if io else None,
            "packets_recv": io.packets_recv if io else None,
        })

    return {"interfaces": interfaces}


if __name__ == "__main__":
    import json
    print(json.dumps(get_network_info(), indent=2))