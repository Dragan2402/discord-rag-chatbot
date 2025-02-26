import argparse


def extract_arguments() -> tuple[bool, bool]:
    parser = argparse.ArgumentParser(description="Discord Chat Bot")
    parser.add_argument(
        "--pre_delete_data",
        action="store_true",
        help="Set to true to pre-delete data (default: False)",
    )

    parser.add_argument(
        "--seed_data",
        action="store_true",
        help="Set to seed data (default: False)",
    )

    args = parser.parse_args()

    return args.seed_data, args.pre_delete_data
