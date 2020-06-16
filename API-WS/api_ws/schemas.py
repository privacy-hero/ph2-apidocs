"""Standard Message Schemas and Fields."""

from .util import mls
from .tags import TAGS

# =====================================================================


class Field:
    """A collection of standard field we can re-use."""

    @staticmethod
    def message_type(value=None, desc=None):
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
    @staticmethod
    def tstamp(desc=None):
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

    # -------------------------------------------------------------------------
    @staticmethod
    def url(name="url", desc="A URL"):
        """Return the definition of the standard URL type field."""
        return f"""
            "{name}" : {{
                "type" : "string",
                "format": "url",
                "description" :{mls(desc)}
            }}
        """

    # -------------------------------------------------------------------------
    @staticmethod
    def string(name="string", desc="A STRING", minlength=0, maxlength=0):
        """Return the definition of the standard string field."""
        minlen = ""
        maxlen = ""
        if minlength > 0:
            minlen = f',\n "minLength": {minlength}'
        if maxlength > 0:
            maxlen = f',\n "maxLength": {maxlength}'

        return f"""
            "{name}" : {{
                "type" : "string",
                "description" :{mls(desc)}
                {minlen}
                {maxlen}
            }}
        """

    # -------------------------------------------------------------------------
    @staticmethod
    def enum(name="enum", desc="A ENUM", values=None):
        """Return the definition of the standard string enum field."""
        if values is None:
            values = []
        sep = ""
        enum_string = "["
        for val in values:
            enum_string += f'{sep}"{val}"'
            sep = ","
        enum_string += "]"

        return f"""
            "{name}" : {{
                "type" : "string",
                "description" :{mls(desc)},
                "enum": {enum_string}
            }}
        """

    # -------------------------------------------------------------------------
    @staticmethod
    def int(name="int", inttype="int", desc="A INT", minvalue=None, maxvalue=None):
        """Return the definition of the standard int field."""
        minval = ""
        maxval = ""
        if minvalue is not None:
            minval = f',\n "minValue": {minvalue}'
        if maxvalue is not None:
            maxval = f',\n "maxLength": {maxvalue}'

        return f"""
            "{name}" : {{
                "type" : "int",
                "format" : "{inttype}",
                "description" :{mls(desc)}
                {minval}
                {maxval}
            }}
        """

    # -------------------------------------------------------------------------
    @staticmethod
    def int64(name="int64", desc="A INT64", minvalue=None, maxvalue=None):
        """Return the definition of the standard int64 field."""
        return Field.int(name, "int64", desc, minvalue, maxvalue)

    # -------------------------------------------------------------------------
    @staticmethod
    def int32(name="int32", desc="A INT32", minvalue=None, maxvalue=None):
        """Return the definition of the standard int32 field."""
        return Field.int(name, "int32", desc, minvalue, maxvalue)

    # -------------------------------------------------------------------------
    @staticmethod
    def int_array(
        name="int",
        desc="A INT",
        inttype="int64",
        item_desc=None,
        minitems=1,
        maxitems=None,
        minvalue=None,
        maxvalue=None,
    ):
        """Return the definition of the standard int array field."""
        minval = ""
        maxval = ""
        maxit = ""
        minit = ""
        itdesc = ""
        if minvalue is not None:
            minval = f',\n "minValue": {minvalue}'
        if maxvalue is not None:
            maxval = f',\n "maxValue": {maxvalue}'
        if minitems is not None:
            minit = f',\n "minItems": {minitems}'
        if maxitems is not None:
            maxit = f',\n "maxItems": {maxitems}'
        if item_desc is not None:
            itdesc = f',\n"description": {mls(item_desc)}'

        return f"""
            "{name}" : {{
                "type" : "array",
                "description" :{mls(desc)},
                "items" : {{
                    "type": "int",
                    "format" : "{inttype}"
                    {itdesc}
                    {minval}
                    {maxval}
                }}
                {minit}
                {maxit}
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
            {Field.message_type(mtype, mdesc)},
            {Field.tstamp(tdesc)}
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


def base_message(  # pylint: disable=too-many-arguments
    cmd,
    name,
    title,
    summary,
    description,
    tags,
    tstamp_desc=None,
    extra_fields=None,
    extra_example=None,
    extra_required=None,
):
    """Generate a full message based on the base message."""
    return f"""
        "name" : "{name}",
        "title" : "{title}",
        "summary" : "{summary}",
        "description" : {mls(description)},
        {TAGS.field(tags)},
        "payload" : {{
            { base_message_schema(
                cmd,
                summary,
                tstamp_desc,
                extra_fields,
                extra_example,
                extra_required) },
            "additionalProperties": false
        }}
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
            mfield = ""
            first = True
            for msg in msgs:
                if not first:
                    mfield += ",\n"
                mfield += f"{{ {msg} }}"
                first = False
            return mfield

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
