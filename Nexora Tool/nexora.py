#!/usr/bin/env python3

import argparse
import json
import sys

from nexora_tool.banner import show_banner
from nexora_tool.modules import (
    NexoraError,
    lookup_domain,
    lookup_ip,
    lookup_telegram,
    quick_osint_probe,
    search_name,
    validate_email,
    validate_phone,
)


def print_result(label, data):
    print(f"\n[{label}]")
    print(json.dumps(data, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Nexora Tool - public OSINT utility CLI")
    parser.add_argument("--ip", help="Check IP metadata")
    parser.add_argument("--telegram", help="Look up Telegram username/public profile")
    parser.add_argument("--domain", help="Check DNS/public domain info")
    parser.add_argument("--name", help="Search uses for person name")
    parser.add_argument("--phone", help="Validate phone number")
    parser.add_argument("--email", help="Validate email")
    parser.add_argument("--query", help="Auto-detect query type")
    args = parser.parse_args()

    show_banner()

    try:
        if args.ip:
            print_result("IP LOOKUP", lookup_ip(args.ip))
        elif args.telegram:
            print_result("TELEGRAM LOOKUP", lookup_telegram(args.telegram))
        elif args.domain:
            print_result("DOMAIN LOOKUP", lookup_domain(args.domain))
        elif args.name:
            print_result("PERSON SEARCH", search_name(args.name))
        elif args.phone:
            print_result("PHONE VALIDATION", validate_phone(args.phone))
        elif args.email:
            print_result("EMAIL VALIDATION", validate_email(args.email))
        elif args.query:
            print_result("AUTO PROBE", quick_osint_probe(args.query))
        else:
            print("\nUsage:")
            print("  python3 nexora.py --ip 8.8.8.8")
            print("  python3 nexora.py --telegram username")
            print("  python3 nexora.py --domain example.com")
            print("  python3 nexora.py --name \"John Doe\"")
            print("  python3 nexora.py --phone \"+1 555 123 4567\"")
            print("  python3 nexora.py --email user@example.com")
            print("  python3 nexora.py --query \"john doe\"")
            print("\nNote: Use only for legal, ethical, and authorized research.")
    except NexoraError as exc:
        print(f"\n[ERROR] {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"\n[ERROR] Unexpected issue: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
