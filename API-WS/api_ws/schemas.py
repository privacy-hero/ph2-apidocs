"""Standard Message Schemas and Fields."""

from .util import mls
from .tags import TAGS

# =====================================================================


def message_type_field(value=None, desc=None):
    """Return the definition of the standard message type field."""
    description = """
        This is the name of the message.  The operation that is to be performed
        and the further fields contained within the message can be identified
        based solely on this message type string.
        """
    if desc is None:
        desc = description
    value_str = ""
    if value is not None:
        value_str = f',"const" : "{value}"'
    return f"""
        "message" : {{
            "type" : "string",
            "description" :{mls(desc)}
            {value_str}
        }}
    """


# -------------------------------------------------------------------------
def tstamp_field(desc=None):
    """Return the definition of the standard tstamp field."""
    description = """
        Every adapter/backend generated message contains a unique **tstamp**
        field.  This field defines both the time of a particular event having
        ocurred, and the pairing of messages in the case of events which are
        triggered as a result of commands from the backend.

        An Adapter will always return the tstamp of any message it is
        replying to.  IF the Adapter is generating an event asynchronously
        and not as a result of a direct comment, the tstamp contains the time
        of the event as generated by the adapter.

        The Field is an integer and is the number of **milliseconds** since
        midnight 1970, UTC.  Otherwise known as the Unix Epoch.
        """
    if desc is None:
        desc = description
    return f"""
        "tstamp" : {{
            "type" : "int",
            "format": "int64",
            "description" :{mls(desc)}
        }}
    """


# =====================================================================


def base_message_schema(
    mtype=None,
    mdesc=None,
    tdesc=None,
    extra_fields=None,
    extra_example=None,
    extra_required=None,
):
    """Return the base message schema."""
    exf = ""
    if extra_fields is not None:
        exf = f", {extra_fields}"

    exe = ""
    if extra_example is not None:
        exe = f", {extra_example}"

    example_msg = "example"
    if mtype is not None:
        example_msg = mtype

    exr = ""
    if extra_required is not None:
        exr = f", {extra_required}"

    return f"""
        "type" : "object",
        "properties" : {{
            {message_type_field(mtype, mdesc)},
            {tstamp_field(tdesc)}
            {exf}
        }},
        "example" : {{
            "message" : "{example_msg}",
            "tstamp"  : 1592217870123
            {exe}
        }},
        "required" : [
            "message"
            {exr}
        ]
    """


# =====================================================================


def channel(
    desc, name, sub_desc=None, sub_msgs=None, pub_desc=None, pub_msgs=None, tags=None
):
    """Generate a channel field.

    Args:
        desc (str): channel description
        name (str): channel name
        sub_desc (str, optional): Subscribe messages description.
        sub_msgs (list, optional): List of subscribe messages.
        pub_desc (str, optional): Publish messages description.
        pub_msgs (str, optional): List of publish messages.
    """

    def msg_list(pubsub, name, desc, msgs, tags):
        def expand_msgs(msgs):
            if not isinstance(msgs, list):
                msgs = [msgs]
            field = ""
            first = True
            for msg in msgs:
                if not first:
                    field += ",\n"
                field += f"{{ {msg} }}"
                first = False
            return field

        if msgs is None:
            return ""
        if tags is None:
            tags = ""
        else:
            tags = f",\n{TAGS.field(tags)}"

        return f""",\n
            "{pubsub}": {{
                "summary": "{name}",
                "description": {mls(desc)},
                "message" : {{
                    "oneOf" : [
                        {expand_msgs(msgs)}
                    ]
                }}
                {tags}
            }}
            """

    sub_name = f"{name}"
    pub_name = f"{name}"

    return f"""
        "description": {mls(desc)}
        { msg_list("subscribe", sub_name, sub_desc, sub_msgs, tags) }
        { msg_list("publish", pub_name, pub_desc, pub_msgs, tags) }
    """
