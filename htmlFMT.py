#!/usr/bin/env python3
import argparse
import sys
import os
from bs4 import BeautifulSoup


def clean_html_file(input_path, output_path=None, quiet=False):
    """
    Reads an HTML file, cleans the formatting using BeautifulSoup, and outputs the result.

    Args:
        input_path (str): Path to the source HTML file.
        output_path (str): Optional path to save the cleaned HTML. If None, prints to stdout.
        quiet (bool): If True, suppresses status messages to stderr.
    """
    if not os.path.isfile(input_path):
        print(f"Error: The input file '{input_path}' was not found.", file=sys.stderr)
        sys.exit(1)

    try:
        with open(input_path, "r", encoding="utf-8") as f:
            content = f.read()

        soup = BeautifulSoup(content, "html.parser")

        if not quiet:
            title = soup.title.string if soup.title else "No Title Found"
            links = [
                link.get("href") for link in soup.find_all("link", rel="canonical")
            ]
            meta_info = (
                f"--- Processing: {input_path} ---\n"
                f"Title: {title}\n"
                f"Canonical Link: {links[0] if links else 'Not found'}\n"
            )
            # Write metadata to stderr so it doesn't interfere if stdout is piped
            print(meta_info, file=sys.stderr)

        formatted_html = soup.prettify()

        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(formatted_html)

            if not quiet:
                print(f"Success! Cleaned HTML saved to: {output_path}", file=sys.stderr)
        else:
            print(formatted_html)

    except Exception as e:
        print(f"Error processing {input_path}: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Clean up HTML files using BeautifulSoup.",
        epilog="Example: ./cleanHtml.py -i raw.html -o clean.html",
    )

    parser.add_argument(
        "-i",
        "--in",
        required=True,
        dest="input_path",
        help="Path to the input HTML file",
    )
    parser.add_argument(
        "-o",
        "--out",
        required=False,
        dest="output_path",
        help="Path to save the cleaned HTML file",
    )
    parser.add_argument(
        "-q", "--quiet", action="store_true", help="Suppress status messages"
    )

    # If no arguments are provided, display help and exit
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    clean_html_file(args.input_path, args.output_path, args.quiet)
