"""AsyncAPI Main Defintions.

Privacy Hero 2 - Websocket API - Common Channel Definition.

"""

from .util import mls
from .common_channel import message_type_field


def aws_internal_server_error():
    """Return AWS Internal Server Error Message Structure."""
    description = """
        This message is generated directly by AWS, and does not contain a tstamp.

        This messages indicates something fatal has ocurred in the server.  Upon
        receipt, the adapter should record the fact it ocurred, and try and reconnect
        to the backend, if a successful reconnection occurs, the adapter should log
        the internal server error to the backend, and then continue.
        """

    return f"""
        "name" : "AWSInternalServerError",
        "title" : "AWS Internal Server Error",
        "summary" : "AWS Internal Server Error",
        "description" : {mls(description)},
        "tags" : [
            {{"name":"AWS Errors"}}
        ],
        "payload" : {{
            "type" : "object",
            "properties" : {{
                {message_type_field("Internal server error",
                                    "An internal server error, AWS Generated")},
                "connectionId" : {{
                    "type" : "string",
                    "description" : "The AWS Websocket Connection ID."
                }},
                "requestId" : {{
                    "type" : "string",
                    "description" : "The ID of the request which caused the error."
                }}
            }},
            "example" : {{
                "message" : "Internal server error",
                "connectionId"  : "d2Vic29ja2V0IElE",
                "requestId" : "cmVxdWVzdCBJRA"
            }},
            "required" : [
                "message",
                "connectionId",
                "requestId"
            ],
            "additionalProperties": false
        }}
    """


def aws_server_error():
    """Return AWS General Server Error Message Structure."""
    description = """
        This message is generated directly by AWS, and does not contain a tstamp.

        This messages indicates something fatal has ocurred in the server.  Upon
        receipt, the adapter should record the fact it ocurred, and try and reconnect
        to the backend, if a successful reconnection occurs, the adapter should log
        the internal server error to the backend, and then continue.
        """

    return f"""
        "name" : "AWSServerError",
        "title" : "AWS Server Error",
        "summary" : "AWS Server Error",
        "description" : {mls(description)},
        "tags" : [
            {{"name":"AWS Errors"}}
        ],
        "payload" : {{
            "type" : "object",
            "properties" : {{
                {message_type_field("Error",
                                    "A general server error, AWS Generated")},
                "error" : {{
                    "type" : "string",
                    "description" : "The description of the Error."
                }}
            }},
            "example" : {{
                "message" : "Error",
                "error"  : "An error ocurred."
            }},
            "required" : [
                "message",
                "error"
            ],
            "additionalProperties": false
        }}
    """


def backend_channel():
    """Messages/message formats which are common between the backend and adapter."""
    description = """
        This is the message channel from the backend to the adapter.  The backend will
        typically contact the adapter in reply to a request from the adapter itself,
        or a request from the client interacting with the backend.

        Most communication from the backend operates as a state machine.  The backend
        will set a tstamp in a message and send the message to the adapter, once the
        adapter has executed the operation, it will reply with a state change that
        reflects the tstamp in the message which triggered it.

    """

    return f"""
        "description": {mls(description)},
        "publish": {{
            "summary" : "Backend Messages.",
            "description": "Message from the Backend to the Adapter.",
            "message" : {{
                "oneOf" : [
                   {{ {aws_internal_server_error()} }},
                   {{ {aws_server_error()} }}
                ]
            }}
        }}
    """
