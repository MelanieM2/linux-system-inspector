import argparse # this is a Python's standard library module for building command line interfaces. 
import sys
from pathlib import Path # pathlib is Python's modern way of working with file paths.

from inspector.cpu import get_cpu_info
from inspector.ram import get_ram_info
from inspector.disk import get_disk_info
from inspector.network import get_network_info
from inspector.os_info import get_os_info
from reporter import generate_report


def parse_args():
    """Define and parse command line arguments."""
    
    
    # ArgumentParser is the main class of argparse. We instantiate it once
    parser = argparse.ArgumentParser(
        prog="inspector",
        description="Linux System Inspector — reports CPU, RAM, disk, network and OS info.",
    ) # prog sets the name shown in help text, and 'description' accepts a string to be shown at the top output when runing --help

    parser.add_argument("--cpu",     action="store_true", help="Include CPU info") # no value, just presence
                                                                                   # action="store_true" means this is a flag — a switch that is either present or absent.
                                                                                   # When the user writes --cpu, args.cpu becomes True. 
                                                                                   # When they don't write it, args.cpu is False. 
                                                                                   # No value is needed after the flag — it's binary.

    parser.add_argument("--ram",     action="store_true", help="Include RAM info") 
    parser.add_argument("--disk",    action="store_true", help="Include disk info")
    parser.add_argument("--network", action="store_true", help="Include network info")
    parser.add_argument("--os",      action="store_true", help="Include OS info")

    parser.add_argument(
        "--format",
        choices=["md", "json"],
        default="md",
        help="Output format: md (default) or json",
    ) # value required

    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Save report to this file path instead of printing to terminal",
    ) # value required

    return parser.parse_args()


def collect_data(args) -> dict:
    """Call inspector modules based on selected flags.
    
    If no module flags are given, collect everything.
    """

    # any() returns True and hence collect_all False, if at least one item in the list is truthy. 
    # If no specific flags given, then collect_all True, and hence by default it calls all modules
    collect_all = not any([args.cpu, args.ram, args.disk, args.network, args.os])

    data = {}

    # Below, if the user passed --cpu, then args.cpu is True, then 
    # any() returns True, not True gives collect_all = False. 
    # This means only run what was explicitly requested. 
    # This single line replaces what would otherwise be a complex chain of if/else conditions
    if collect_all or args.cpu:
        print("Collecting CPU info...", file=sys.stderr)
        data["cpu"] = get_cpu_info()

    # stderr — standard error in Unix. This is where status messages, warnings, and progress info go.
    # stdout — standard output. This is where the actual report goes.

    if collect_all or args.ram:
        print("Collecting RAM info...", file=sys.stderr)
        data["ram"] = get_ram_info()

    if collect_all or args.disk:
        print("Collecting disk info...", file=sys.stderr)
        data["disk"] = get_disk_info()

    if collect_all or args.network:
        print("Collecting network info...", file=sys.stderr)
        data["network"] = get_network_info()

    if collect_all or args.os:
        print("Collecting OS info...", file=sys.stderr)
        data["os"] = get_os_info()

    return data


def main():
    """Main entry point — orchestrates collection, formatting and output."""

    args = parse_args()
    data = collect_data(args)
    report = generate_report(data, fmt=args.format)

    if args.output:
        output_path = Path(args.output)  # Path objects are smarter than raw strings.
                                         # they handle path separators correctly 
                                         # across operating systems and have useful methods built in.
        output_path.write_text(report, encoding="utf-8") # write_text() opens the file, writes the string, and closes it, all in one call. 
                                                         # ensures consistent text encoding regardless of system defaults.
        print(f"Report saved to {output_path}", file=sys.stderr)
    else:
        print(report)


if __name__ == "__main__":
    main()
