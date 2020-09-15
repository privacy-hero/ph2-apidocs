"""Websocket API Generation Script."""
import subprocess
import os
import sys
import json
import traceback
from pathlib import Path

import click
import jsonschema

from .api import ws_api

# ------------------------------------------------------------------------------


def validate_asynapi(filename: str):
    """Read a json file and validate against a schema."""
    try:
        schema_path = Path(__file__).parent / ".." / "json" / "asyncapi.schema.json"
        data_path = Path(__file__).parent / ".." / filename
        schema = json.loads(schema_path.read_text())
        schema = json.loads(schema_path.read_text())

        data = json.loads(data_path.read_text())
        validator = jsonschema.Draft7Validator(schema)

        cnt = 0
        for error in validator.iter_errors(data):
            cnt += 1
            print(f"{filename} ERROR {cnt}:\n{error}")
    except Exception:  # pylint:disable=broad-except
        print(traceback.format_exc())
        sys.exit(1)


# ------------------------------------------------------------------------------


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


# ------------------------------------------------------------------------------


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


# ------------------------------------------------------------------------------


@click.group()
def cli():
    """Remains empty, just for the command line option parser."""


CONTEXT_LINES = 10

# ------------------------------------------------------------------------------


def print_file_linenos(dump, lineno, col, msg):
    """Print the file in the multi-line dump string with line numbers."""
    linecount = 1
    this = "  "
    for line in dump.splitlines():
        if linecount == lineno:
            this = "->"
        if (lineno - CONTEXT_LINES) <= linecount <= (lineno + CONTEXT_LINES):
            print(f"{this} {linecount:5} : {line}")
        if linecount == lineno:
            print(f'{" "*(col+11)}^ {msg}')
        linecount += 1
        this = "  "


# ------------------------------------------------------------------------------


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
    # We validate against the json-schema
    validate_asynapi("json/asyncapi.json")
    # And also an external tool because it finds more errors.
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


# ------------------------------------------------------------------------------

if __name__ == "__main__":
    cli()
