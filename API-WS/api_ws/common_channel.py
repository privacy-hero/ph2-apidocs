"""AsyncAPI Main Defintions.

Privacy Hero 2 - Websocket API - Common Channel Definition.

"""

from .util import mls
from .tags import TAGS
from .schemas import base_message_schema, channel


def multi_field():
    """Return Multiple message packet field."""
    description = """
        An array of complete and individual messages as defined elsewhere in
        this specification.
        """
    return f"""
        "msgs": {{
            "type": "array",
            "description": {mls(description)},
            "items": {{ {base_message_schema()} }},
            "minItems": 1,
            "maxItems": 32
        }}
    """


def base_message():
    """Return Standard Base Message Structure."""
    description = """
        All Privacy Hero 2 system messages have the following standard form.
        """

    return f"""
        "name" : "BaseMsg",
        "title" : "Base Message",
        "summary" : "Standard Message Base Format",
        "description" : {mls(description)},
        "tags" : [
            {TAGS.get(TAGS.MSG_FORMATS)}
        ],
        "payload" : {{
            {base_message_schema()}
        }}
    """


def multi_message():
    """Return Standard Multi Message Structure."""
    description = """
        All Privacy Hero 2 system messages may be bundled into a single multi-message.
        The multi message is a standard message, which hold an array of individual
        messages.  The individual messages when received will be treated as if they
        were received sequentially and independently in the order they are listed.

        The purpose of a Multi-Message is to cluster message processing for efficiency.
        """

    tstamp_desc = """
        The time the message was generated, unrelated to the bundled messages
        timestamps.
    """

    extra_fields = f"{multi_field()}"
    extra_example = '"msgs" : []'
    extra_required = '"tstamp", "msgs"'

    return f"""
        "name" : "MultiMsg",
        "title" : "Multi Message",
        "summary" : "Multiple Message Packet",
        "description" : {mls(description)},
        "tags" : [
            {TAGS.get(TAGS.MSG_FORMATS)}
        ],
        "payload" : {{
            { base_message_schema(
                "multi",
                "Multiple Message Packet.",
                tstamp_desc,
                extra_fields,
                extra_example,
                extra_required) },
            "additionalProperties": false
        }}
    """


def common_channel():
    """Messages/message formats which are common between the backend and adapter."""
    description = """
        The common channel is not an actual channel.  It defines the basic message
        structure upon which all other messages are based.
    """

    publish_desc = """
        All messages are sent by each end of the websocket as required.  These message
        formats are equally valid for transmission from the adapter [SUB] as well as
        transmission by the back end [PUB].

        There is no strict Subscribe/Publish semantic it is documentation convention
        ONLY. The websocket acts as two unidirectional message pipes and Sub/Pub
        messages are formatted, sent, received and treated identically and without
        distinction.
    """

    publish_msgs = [base_message(), multi_message()]

    return channel(
        description,
        "Basic Message Forms",
        sub_desc=publish_desc,
        sub_msgs=publish_msgs,
        pub_desc=publish_desc,
        pub_msgs=publish_msgs,
        tags=TAGS.MSG_FORMATS,
    )
