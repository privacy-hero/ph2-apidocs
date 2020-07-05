"""Websocket API Generation Script."""
import subprocess
import os
import sys

import click

from .api import ws_api


def gen_directly(input_file, output_dir):
    """Generate the HTML file by calling the generator directly."""
    subprocess.check_output(
        [
            "asyncapi-generator",
            "--force-write",
            "-p",
            "sidebarOrganization=byTags",
            "-o",
            output_dir,
            input_file,
            "@asyncapi/html-template",
        ]
    )


def gen_by_docker(input_file, output_dir):
    """Generate the HTML file by using a docker instance."""
    subprocess.check_output(
        [
            "docker",
            "run",
            "--rm",
            "-it",
            "-v",
            f"{input_file}:/app/asyncapi.json",
            "-v",
            f"{output_dir}:/app/output",
            "asyncapi/generator",
            "/app/asyncapi.json",
            "@asyncapi/html-template",
            "-o",
            "/app/output",
            "--force-write",
            "-p",
            "sidebarOrganization=byTags",
        ]
    )


@click.group()
def cli():
    """Remains empty, just for the command line option parser."""


def print_file_linenos(dump, lineno, col, msg):
    """Print the file in the multi-line dump string with line numbers."""
    linecount = 1
    this = "  "
    for line in dump.splitlines():
        if linecount == lineno:
            this = "->"
        if (lineno - 6) >= linecount <= (lineno + 6):
            print(f"{this} {linecount:5} : {line}")
        if linecount == lineno:
            print(f'{" "*(col+11)}^ {msg}')
        linecount += 1
        this = "  "


@cli.command()
def make_docs():
    """Make the AsyncAPI Websocket Documentation."""
    print("Generating API JSON File...")
    raw_api = ws_api()

    print("Checking for valid JSON...")
    # Check we made valid json
    try:
        json_fmt_api = subprocess.check_output(
            ["jsonlint", "--compact"], input=raw_api.encode(), stderr=subprocess.STDOUT
        )
    except subprocess.CalledProcessError as ex:
        print("ERROR:")
        print(ex.output.decode().strip())
        err = ex.output.decode().split(" ", 4)
        lineno = int(err[1][:-1])
        col = int(err[3][:-1])
        msg = err[4].strip()
        print("------------------------------------------------------")
        print_file_linenos(raw_api, lineno, col, msg)
        sys.exit(1)

    with open("./json/asyncapi.json", "w") as text_file:
        text_file.write(json_fmt_api.decode())

    print("Checking for valid ASYNCAPI...")
    # Check we made a valid asyncapi file
    try:
        subprocess.check_output(["node", "./validate-asyncapi.js"])
    except subprocess.CalledProcessError as ex:
        print("ERROR:")
        print(ex.output.decode())
        sys.exit(1)

    print("Generating HTML...")
    # Generate HTML Version - use docker because native ag has issues.
    input_file = os.path.abspath("json/asyncapi.json")
    output_dir = os.path.abspath("html")

    try:
        gen_directly(input_file, output_dir)
    except subprocess.CalledProcessError as ex:
        print("ERROR:")
        print(ex.output.decode())
        sys.exit(1)


if __name__ == "__main__":
    cli()
