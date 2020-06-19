"""Standard Message Schemas and Fields."""
import json
import hashlib
from base64 import urlsafe_b64encode

from .util import mls, KB
from .tags import TAGS

# =====================================================================


def sha256_example(text):
    """Generate a proper base64url encoded sha256 hash."""
    return urlsafe_b64encode(hashlib.sha256(text.encode()).digest()).decode()[:-1]


# =====================================================================


class Field:
    """A collection of standard field we can re-use."""

    @staticmethod
    def named(name=None, field=""):
        """Warp a field with a name, if it has one."""
        if name is None:
            return field
        return f"""
            "{name}" : {{
                {field}
            }}
        """

    # -------------------------------------------------------------------------

    @staticmethod
    def optional(name="optional", value=None, omitif=None, quote='"'):
        """Omit optional fields if they are not relevant."""
        if (omitif is None) and (value is None):
            return ""
        if value == omitif:
            return ""
        return f',\n "{name}": {quote}{value}{quote}'

    # -------------------------------------------------------------------------

    @staticmethod
    def message_type(value="message", desc=None):
        """Return the definition of the standard message type field."""
        description = """
            This is the name of the message.  The operation that is to be performed
            and the further fields contained within the message can be identified
            based solely on this message type string.
        """
        if desc is None:
            desc = description
        if value is None:  # if no message type is specified, don't emit a constant
            return Field.string("message", desc)
        return Field.const_string("message", desc, value)

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
        return Field.timestamp_ms("tstamp", desc)

    # -------------------------------------------------------------------------
    @staticmethod
    def timestamp_ms(name="timestamp_ms", desc="A Millisecond Timestamp"):
        """Return the definition of the standard tstamp field."""
        return Field.named(
            name,
            f"""
                "type" : "int",
                "format": "int64",
                "description" :{mls(desc)}
            """,
        )

    # -------------------------------------------------------------------------
    @staticmethod
    def url(name="url", desc="A URL"):
        """Return the definition of the standard URL type field."""
        return Field.named(
            name,
            f"""
                "type" : "string",
                "format": "url",
                "description" :{mls(desc)}
            """,
        )

    # -------------------------------------------------------------------------
    @staticmethod
    def ipv4(name="ipv4", desc="A IPv4 Address"):
        """Return the definition of the standard IPv4 type field."""
        return Field.named(
            name,
            f"""
                "type" : "string",
                "format": "IPv4 Address",
                "description" :{mls(desc)},
                "minLength": {len("0.0.0.0")},
                "maxLength": {len("255.255.255.255")}
            """,
        )

    # -------------------------------------------------------------------------
    @staticmethod
    def ipv6(name="ipv6", desc="A IPv6 Address"):
        """Return the definition of the standard IPv4 type field."""
        return Field.named(
            name,
            f"""
                "type" : "string",
                "format": "IPv6 Address",
                "description" :{mls(desc)},
                "minLength": {len("::")},
                "maxLength": {len("FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF")}
            """,
        )

    # -------------------------------------------------------------------------
    @staticmethod
    def mac(name="mac", desc="A Mac Address"):
        """Return the definition of the standard Mac type field."""
        return Field.named(
            name,
            f"""
                "type" : "string",
                "format": "Mac EUI",
                "description" :{mls(desc)},
                "minLength": 1,
                "maxLength": {len("00:11:22:33:44:55")}
            """,
        )

    # -------------------------------------------------------------------------
    @staticmethod
    def sha256(name="sha256", desc="A Base64-URL Encoded SHA256 hash"):
        """Return the definition of the standard sha256 type field."""
        return Field.named(
            name,
            f"""
                "type" : "string",
                "format": "bas64-url-sha256",
                "description" :{mls(desc)},
                "minLength": 43,
                "maxLength": 43
            """,
        )

    # -------------------------------------------------------------------------
    @staticmethod
    def binary(name="binary", desc="A Base64-URL Encoded binary blob"):
        """Return the definition of the standard base64-url binary type field."""
        return Field.named(
            name,
            f"""
                "type" : "string",
                "format": "bas64-url-binary",
                "description" :{mls(desc)},
                "minLength": 1,
                "maxLength": {KB(120)}
            """,
        )

    # -------------------------------------------------------------------------
    @staticmethod
    def const_string(name="string", desc="A CONSTANT", value="const"):
        """Return the definition of the standard constant string field."""
        return Field.named(
            name,
            f"""
                "type" : "string",
                "description" :{mls(desc)},
                "const" : "{value}",
                "minLength": {len(value)},
                "maxLength": {len(value)}
            """,
        )

    # -------------------------------------------------------------------------
    @staticmethod
    def string(name="string", desc="A STRING", minlength=0, maxlength=0, fmat=None):
        """Return the definition of the standard string field."""
        return Field.named(
            name,
            f"""
                "type" : "string",
                "description" :{mls(desc)}
                {Field.optional("minLength", minlength, 0, "")}
                {Field.optional("maxLength", maxlength, 0, "")}
                {Field.optional("format", fmat)}
            """,
        )

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

        return Field.named(
            name,
            f"""
                "type" : "string",
                "description" :{mls(desc)},
                "enum": {enum_string}
            """,
        )

    # -------------------------------------------------------------------------
    @staticmethod
    def int(name="int", inttype="int", desc="A INT", minvalue=None, maxvalue=None):
        """Return the definition of the standard int field."""
        return Field.named(
            name,
            f"""
                "type" : "int",
                "format" : "{inttype}",
                "description" :{mls(desc)}
                {Field.optional("minValue", minvalue, quote="")}
                {Field.optional("maxValue", maxvalue, quote="")}
            """,
        )

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
    def array(
        name="array", desc="AN ARRAY", items="{}", minitems=1, maxitems=None,
    ):
        """Return the definition of the standard array field."""
        return Field.named(
            name,
            f"""
                "type" : "array",
                "description" :{mls(desc)},
                "items" : {{
                    {items}
                }}
                {Field.optional("minItems",minitems, quote="")}
                {Field.optional("maxItems",maxitems, quote="")}
            """,
        )

    # -------------------------------------------------------------------------
    @staticmethod
    def boolean(name="boolean", desc="A BOOL"):
        """Return the definition of the standard boolean field."""
        return Field.named(
            name,
            f"""
                "type" : "boolean",
                "description" :{mls(desc)}
            """,
        )

    # -------------------------------------------------------------------------
    @staticmethod
    def uuid(name="uuid", desc="A UUID"):
        """Return the definition of the standard boolean field."""
        uuidlen = len("85647580-68ec-44da-8bc8-3e7b8cf7b0e6")
        return Field.string(name, desc, uuidlen, uuidlen, "UUID")

    # -------------------------------------------------------------------------
    @staticmethod
    def object(
        name="object", desc="A OBJECT", required=[], fields="{}", additional=False
    ):  # pylint: disable=dangerous-default-value
        """Return a object."""
        additional = str(additional).lower()
        return Field.named(
            name,
            f"""
                "type" : "object",
                "required": {json.dumps(required)},
                "description" :{mls(desc)},
                "properties" : {fields}
                {Field.optional("additionalProperties", additional, "true", quote="")}
            """,
        )


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
