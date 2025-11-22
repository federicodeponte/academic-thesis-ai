"""Command-line interface for OpenDraft."""

import sys
import argparse
from opendraft.version import __version__


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="opendraft",
        description="AI-Powered Academic Writing Framework",
        epilog="For more information, visit: https://github.com/federicodeponte/opendraft"
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Verify command
    verify_parser = subparsers.add_parser(
        "verify",
        help="Verify installation and configuration"
    )

    # Generate command (placeholder for future implementation)
    generate_parser = subparsers.add_parser(
        "generate",
        help="Generate a thesis (coming soon)"
    )
    generate_parser.add_argument(
        "--topic",
        type=str,
        help="Research topic"
    )

    args = parser.parse_args()

    if args.command == "verify":
        from opendraft.verify import verify_installation
        sys.exit(verify_installation())
    elif args.command == "generate":
        print("❌ Thesis generation via CLI is coming soon!")
        print("For now, please use the Python API or test scripts.")
        print("See: https://github.com/federicodeponte/opendraft#quick-start")
        sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
