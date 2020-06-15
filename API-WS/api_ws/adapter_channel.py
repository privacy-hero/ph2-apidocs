"""AsyncAPI Main Defintions.

Privacy Hero 2 - Websocket API - Common Channel Definition.

"""

from .util import mls


def base_message():
    """Return Base Message Structure."""
    return f"""
        "name" : "BaseRouterMsg",
        "title" : "Base Router Message",
        "summary" : "Base Router Message Summary",
        "description" : "Basic Message Template Description.",
        "payload" : {{
            "type" : "object",
            "properties" : {{
                "message" : {{
                    "type" : "string"
                }}
            }}
        }}
    """


def adapter_channel():
    """Messages/message formats which are common between the backend and adapter."""
    description = """
        The common channel defines the messages that are either templates of all other
        messages or common to both the backend and the adapter channels.

    """

    return f"""
        "description": {mls(description)},
        "publish": {{
            "summary" : "Adapter Messages.",
            "description": "Message from the Adapter to the Backend.",
            "message" : {{
                "oneOf" : [
                   {{ {base_message()} }}
                ]
            }}
        }}
    """
