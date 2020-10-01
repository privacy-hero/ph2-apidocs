"""AsyncAPI Main Defintions.

Privacy Hero 2 - Websocket API - Adapter WPS Configuration Message Definitions.
"""

# from .util import mls
from .schemas import base_message, channel, Field
from .tags import TAGS
from .xref import Xref


# ------------------------------------------------------------------------------


def wps_status():
    """Advises the Backend of the current status of the WPS Function."""
    cmd = "wps-status"
    name = "WPSStatus"
    title = "WPS Function Status"
    summary = "Report WPS Function Status."

    description = f"""
        This message advises the current WPS Function status to the backend.
        This is a summary of the result of presing the WPS button on the router.

        See {Xref.adapter_service_state} for the configuration which
        enables/disables the WPS function.
    """

    tstamp_desc = """
        The request timestamp of the configuration.
    """

    status_desc = """
    The current status of the WPS function.

    - *activated* = The WPS function is activated.  The optional **duration**
      field defines the number of seconds the WPS mode will be active.
    - *blocked* = The WPS function activation button was pressed, but the
      function is blocked by configuration. **duration** is omitted with this
      status.
    - *completed* = The WPS function is no longer activated. **duration** is
      omitted with this status.
    """

    extra_fields = f"""
        {Field.enum("status", status_desc,["activated", "blocked","completed"])},
        {Field.int("duration", "Number of seconds WPS will be activated on the router.")}
    """

    extra_required = '"tstamp","status"'
    extra_example = """
        "status" : "activated",
        "duration" : 180
    """

    return base_message(
        cmd,
        name,
        title,
        summary,
        description,
        TAGS.ADAPTER_MSGS,
        tstamp_desc,
        extra_fields,
        extra_example,
        extra_required,
    )


# ------------------------------------------------------------------------------


def adapter_wps_configuration_channel():
    """Adapter WPS Config messages."""
    description = """
        These are messages related to the WPS operation of the adapter.

        These messages are sent on initial connection and also periodically as
        required to reflect user changes in the configuration.
    """

    subscribe_desc = "WPS Messages from the Adapter"
    subscribe_msgs = [
        wps_status(),
    ]

    publish_desc = None
    publish_msgs = None

    return channel(
        description,
        "Adapter WPS Configuration",
        sub_desc=subscribe_desc,
        sub_msgs=subscribe_msgs,
        pub_desc=publish_desc,
        pub_msgs=publish_msgs,
        tags=TAGS.ADAPTER_MSGS,
    )
