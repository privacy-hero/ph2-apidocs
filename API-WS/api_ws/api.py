"""AsyncAPI Main Defintions.

Privacy Hero 2 - Websocket API

We use Python f-strings and functions to build out the API.  Which is easier and
more expressive than limiting to any particular template system.

The API is constructed from JSON, as that is easier to generate programatically
as formatting it not important.

NOTE: Literal Json { and }  must be represented as {{ and }} inside the f string.
"""

from .util import mls
from .common_channel import common_channel

from .backend_channel import backend_channel
from .adapter_channel import adapter_channel

TITLE = "Privacy Hero 2 - Adapter <-> Backend Websocket API"
VERSION = "0.0.3"
DESC = mls(
    """
    The API for Adapter to Backend communication.

    All communication is carried out through a single websocket connection per
    adapter.  The Adapter connects and sends updates to state as required, and is
    also triggered to perform operations or update its state asynchronously from
    the backend through the same connection.

    Both directions of the connection use the same basic message format.
    """
)


def info():
    """Return API Basic Information."""
    return f"""
        "title": "{TITLE}",
        "version": "{VERSION}",
        "description": {DESC}
    """


def security():
    """Define the server security."""
    description = """
        The user password follows the form <Adapter MAC>:<Adapter Secret Hash>

        - **Adapter MAC** is the hardware Mac address of the Adapter and it must
            be the same as the mac used to register the adapter in production.
            The MAC has the format *00:11:22:33:44:55* or *001122334455* or
            *00-11-22-33-44-55* all of which are equivalent
        - **Adapter Secret Hash** is a Base64-URL encoded SHA256 hash of the
        unique id contained within the cpu or chips of the adapter.

        An example user:password is (the binary secret is the string ***password*** ):

        *00:11:22:33:44:55:XohImNooBHFR0OVvjcYpJ3NgPQ1qq73WKhHvch0VQtg*

        The user/password is passed in the **Authorization** header of the http
        connection which established the websocket.
        """

    return f"""
        "user-password": {{
            "type": "userPassword",
            "description": {mls(description)}
        }}
        """


def servers():
    """Return The Servers we employ."""
    return """
    "development": {
      "url": "ws2-dev.privacyhero.com",
      "description": "Development server",
      "protocol": "wss",
      "security": [ { "user-password": [ ] } ]
    },
    "qa": {
      "url": "ws2-qa.privacyhero.com",
      "description": "QA Test server",
      "protocol": "wss",
      "security": [ { "user-password": [ ] } ]
    },
    "production": {
      "url": "wss://ws2.privacyhero.com",
      "description": "Production server",
      "protocol": "wss",
      "security": [ { "user-password": [ ] } ]
    }"""


def components():
    """Return The components we reuse in the specification."""
    return f"""
        "securitySchemes": {{ {security()} }}
    """


def channels():
    """Message Channels."""
    return f"""
        "COMMON": {{ {common_channel()} }},
        "BACKEND": {{ {backend_channel()} }},
        "ADAPTER": {{ {adapter_channel()} }}
    """


def ws_api():
    """Return the full websocket API Document as a string."""
    return f"""{{
        "asyncapi": "2.0.0",
        "defaultContentType": "application/json",
        "info": {{ {info()} }},
        "servers": {{ {servers()} }},
        "components": {{ {components()} }},
        "channels": {{ {channels()} }}
    }}
    """
