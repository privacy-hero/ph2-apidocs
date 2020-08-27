"""AsyncAPI Main Defintions.

Privacy Hero 2 - Websocket API - Common Channel Definition.

"""

from .util import mls
from .tags import TAGS
from .schemas import base_message_schema, channel, MsgDirection


def multi_field(direction: MsgDirection = MsgDirection.TX_TO_ROUTER):
    """Return Multiple message packet field."""
    description = """
        An array of complete and individual messages as defined elsewhere in
        this specification.
        """
    return f"""
        "msgs": {{
            "type": "array",
            "description": {mls(description)},
            "items": {{ {base_message_schema(direction=direction)} }},
            "minItems": 1,
            "maxItems": 32
        }}
    """


def base_message(direction: MsgDirection = MsgDirection.TX_TO_ROUTER):
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
            {base_message_schema(direction=direction)}
        }}
    """


def multi_message(direction: MsgDirection = MsgDirection.TX_TO_ROUTER):
    """Return Standard Multi Message Structure."""
    description = """
        All Privacy Hero 2 system messages may be bundled into a single multi-message.
        The multi message is a standard message, which hold an array of individual
        messages.  The individual messages when received will be treated as if they
        were received sequentially and independently in the order they are listed.

        The purpose of a Multi-Message is to cluster message processing for efficiency.

        ## Notes regarding adapter bundling implementation.

        The Backend is charged in 100ms units of execution.  It also takes time for the
        backend to startup and begin processing.  Therefore, it is preferable, unless
        the message is urgent, that all messages are bundled in the adapter in a minimum
        of 200ms blocks.  If an urgent message must be sent, it should be added to
        the current bundle and the entire bundle be sent immediately.

        The maximum single multi-message size must not exceed 32KB.  If adding a message
        to the bundle would cause the message size to exceed 32KB, the bundle should be
        sent and the message which would have exceeded the size is added to the next
        bundle.  IF a message is defined which does exceed 32KB, it should not be
        bundled, but MUST be sent as a discreet message.  In this case, the maximum
        message size must never exceed 128KB.

        The multi-message is guaranteed NOT to have an *id* field, but the
        messages contained within it, may have *id* fields and they should be
        processed accordingly.
        """

    tstamp_desc = """
        The time the message was generated, unrelated to the bundled messages
        timestamps.
    """

    extra_fields = f"{multi_field(direction=direction)}"
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
                extra_required,
                id_field=False) },
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
    subscribe_msgs = [
        base_message(direction=MsgDirection.RX_FROM_ROUTER),
        multi_message(),
    ]

    return channel(
        description,
        "Basic Message Forms",
        sub_desc=publish_desc,
        sub_msgs=publish_msgs,
        pub_desc=publish_desc,
        pub_msgs=subscribe_msgs,
        tags=TAGS.MSG_FORMATS,
    )
