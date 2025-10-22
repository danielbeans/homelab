import argparse
import json
import sys
from pathlib import Path
from typing import Any


def load_daemon_config(config_path: Path) -> dict[str, Any]:
    try:
        with open(config_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Config file {config_path} not found, will create new one.")
        return {}


def save_daemon_config(config_path: Path, config: dict) -> None:
    try:
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)
        print(f"Successfully updated {config_path}")
    except PermissionError:
        print(f"Permission denied. Please run with sudo to modify {config_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error writing to {config_path}: {e}")
        sys.exit(1)


def merge_dns_entries(existing_dns: list[str], new_dns: list[str]) -> list[str]:
    if existing_dns is None:
        return new_dns

    existing_set = set(existing_dns)
    new_set = set(new_dns)

    merged_dns = list(existing_set.union(new_set))
    return merged_dns


def validate_dns_entries(dns_entries):
    for dns in dns_entries:
        parts = dns.split(".")
        if len(parts) != 4 or not all(
            part.isdigit() and 0 <= int(part) <= 255 for part in parts
        ):
            print(f"Warning: '{dns}' doesn't appear to be a valid IPv4 address")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Add DNS entries to Docker daemon configuration"
    )

    parser.add_argument(
        "dns_servers",
        nargs="+",
        help="DNS server IP addresses to add (e.g., 8.8.8.8 8.8.4.4)",
    )

    parser.add_argument(
        "--config",
        type=Path,
        default=Path("/etc/docker/daemon.json"),
        help="Path to daemon.json file",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be changed without making actual changes",
    )

    parser.add_argument(
        "--replace",
        action="store_true",
        help="Replace existing DNS entries instead of merging",
    )

    args = parser.parse_args()

    for dns in args.dns_servers:
        parts = dns.split(".")
        if len(parts) != 4 or not all(
            part.isdigit() and 0 <= int(part) <= 255 for part in parts
        ):
            raise ValueError(
                f"Warning: '{dns}' doesn't appear to be a valid IPv4 address"
            )

    config = load_daemon_config(args.config)
    existing_dns = config.get("dns", [])

    if args.replace:
        new_dns = args.dns_servers
        print(f"Replacing DNS entries: {existing_dns} -> {new_dns}")
    else:
        new_dns = merge_dns_entries(existing_dns, args.dns_servers)
        added_dns = list(set(args.dns_servers) - set(existing_dns))
        if added_dns:
            print(f"Adding new DNS entries: {added_dns}")
        else:
            print("All DNS entries already exist")

    config["dns"] = new_dns

    if args.dry_run:
        print("\nDry run - configuration that would be written:")
        print(json.dumps(config, indent=2))
        print(f"\nWould write to: {args.config}")
    else:
        save_daemon_config(args.config, config)

        print(f"\nFinal DNS configuration: {new_dns}")
        print("Note: You may need to restart Docker daemon for changes to take effect:")
        print("  sudo systemctl restart docker")


if __name__ == "__main__":
    main()
