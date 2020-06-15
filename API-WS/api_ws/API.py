"""AsyncAPI Main Defintions.

Privacy Hero 2 - Websocket API

We use Python f-strings and functions to build out the API.  Which is easier and
more expressive than limiting to any particular template system.

The API is constructed from JSON, as that is easier to generate programatically
as formatting it not important.

NOTE: Literal Json { and }  must be represented as {{ and }} inside the f string.
"""

TITLE = "Privacy Hero 2 - Adapter <-> Backend Websocket API"
VERSION = "0.1"


def info():
    """Return API Basic Information."""
    return f"""
        "title": {TITLE},
        "version": {VERSION}
    """


def security():
    """Define the server security."""
    return """"
    "user-password": {
      "type": "userPassword"
      "description":
"The user password follows the form <Adapter MAC>:<Adapter Secret Hash>
The Adapter MAC is the hardware Mac address of the Adapter and it must be
the same as the mac used to register the adapter in production.

The Adapter Secret Hash is a Base64-URL encoded SHA256 hash of the unique id
contained within the cpu or chips of the adapter.
"
    }

    """


def servers():
    """The Servers we employ."""

    return """
    "development": {
      "url": "ws2-dev.privacyhero.com",
      "description": "Development server",
      "protocol": "wss",
      "security": [ { "user-password": [ ] } ],
    },
    "qa": {
      "url": "ws2-qa.privacyhero.com",
      "description": "QA Test server",
      "protocol": "wss",
      "security": [ { "user-password": [ ] } ],
    },
    "production": {
      "url": "wss://ws2.privacyhero.com",
      "description": "Production server",
      "protocol": "wss",
      "security": [ { "user-password": [ ] } ],
    }"""


def components():
    """The components we reuse in the specification."""
    return f"""
        "securitySchemes": {security()},
    """


def channels():
    """Message Channels."""
    return ""


def ws_api():
    """Return the full websocket API Document as a string."""
    return f"""{{
        "asyncapi": "2.0.0",
        "info": {{ {info()} }},
        "servers": {{ {servers()} }},
        "components": {{ {components()} }},
        "channels": {{ {channels()} }},
    """


"""
    "user/signedup": {{
      "subscribe": {{
        "message": {{
          "description": "An event describing that a user just signed up.",
          "payload": {{
            "type": "object",
            "additionalProperties": false,
            "properties": {{
              "fullName": {{
                "type": "string"
              }},
              "email": {{
                "type": "string",
                "format": "email"
              }},
              "age": {{
                "type": "integer",
                "minimum": 18
              }}
            }}
          }}
        }}
      }}
    }}
  }}
}}
"""
