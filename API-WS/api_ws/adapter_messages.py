"""AsyncAPI Main Defintions.

Privacy Hero 2 - Websocket API - Adapter Diagnostic Message Definitions.
"""

# from .util import mls
from .schemas import base_message, channel, Field, sha256_example
from .adapter_diagnostics import log_level_field
from .tags import TAGS


def link_established():
    """Adapter advice that the websocket link is established."""
    description = """
        This message is sent from the Adapter to the Backend as the very first
        message it sends AFTER establishing any websocket connection to the
        backend.  It allows the backend to perform link connection housekeeping
        for the adapter, which is necessary for proper operation.
    """

    tstamp_desc = """
        The time the link established message was queued by the Adapter.
        (According to the adapters internal clock.)
    """

    version_desc = """
        sha256 hash of the firmware image currently loaded in the Adapter. Encoded
        with base64-url encoding.
    """

    variant_desc = """
        Optional: Identifier to specify what type of operation the adapter is
        performing.  This is used to allow the system to deploy different software
        versions to the same hardware.  Normally the backend will not change the
        variant but will advise about the latest version of software for that variant.
    """

    disconnected_desc = """
        Optional: If this message is being sent because the link was disconnected, the
        **disconnected** field is sent, containing the time in milliseconds when the
        adapter detected the link had failed.  If this is the first connection
        since power on, this field is omitted.
    """

    cmd = "link established"
    name = "LinkEstablished"
    title = "Link Established"
    summary = "Advise the Backend that the Adapter has connected to a new websocket"

    extra_fields = f"""
        {Field.sha256("version", version_desc)},
        {Field.string("variant",variant_desc, minlength=1)},
        {Field.timestamp_ms("disconnected", disconnected_desc)}
    """

    extra_example = f"""
        "version" : "{sha256_example("Firmware Version")}",
        "variant" : "PHero2-Router",
        "disconnected" : 1592316782123
    """

    extra_required = '"tstamp", "version"'

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


def initial_config():
    """Return Initial configuration of the adapter."""
    description = """
        This message contains the highest level configuration and is sent by the
        backend after a link is established, and the backend receives the
        *Link Established* message from the Adapter.
    """

    tstamp_desc = """
        The tstamp in this message is the same tstamp sent in the *Link Established*
        message from the adapter which triggered it to be sent.
    """

    version_desc = """
        The version of the latest firmaware suitable for the adapter.  This
        version should match the version installed in the adapter before it continues.
        If it does noe, the adapter should retrieve the new version from the url in
        this message, program that and restart the connection.
    """

    firmware_desc = """
        The firmware url.  This is the location where the latest firmware may be
        downloaded.  If the adapter detects that a firmware update is required it
        downloads the firmware from this URL.  If the firmware can not be downloaded
        or the image downloaded does not match the **version** hash, then the firmware
        in the adapter must not be changed, and an error should be logged to the
        backend.
    """

    cmd = "initial cfg"
    name = "InitialConfig"
    title = "Initial Configuration"
    summary = "Initial Highest Level Configuration"

    extra_fields = f"""
        {Field.sha256("version", version_desc)},
        {Field.url("firmware", firmware_desc)},
        {log_level_field(none_ok=True, name="loglevel",
         desc="The Minimum level of messages which should be logged to the backend.")}
    """
    extra_example = f"""
        "version": "{sha256_example("New Firmware Hash")}",
        "firmware": "https://dl.privacyhero.com/firmware/adapter_v107.fw",
        "loglevel": "DEBUG"
    """
    extra_required = """
        "tstamp",
        "version",
        "firmware",
        "loglevel"
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


def connection_channel():
    """Define Connection Management messages."""
    description = """
        These are messages related to the websocket connection and its management.

        ## NOTES

        1. AWS will terminate a websocket after remaining idle for 10 minutes.
        2. AWS May terminate a websocket connection that has been continuously
        made for 2 Hours.

        There is nothing preventing the link being immediately re-established.

        ### TODO:

        It is not clear if websocket pings are sufficient to avoid the 10 minute
        idle timeout.  This needs to be tested.

        If it is not sufficient, we will need to do periodic heartbeats at around 9
        minute intervals to prevent the idle timeout.

        It seems there is nothing we can do about the 2 hour timeout except reconnect.
        This timeout needs to be tested.

    """

    subscribe_desc = "Link Management Messages from the Adapter."
    subscribe_msgs = [link_established()]

    publish_desc = "Initial Configuration."
    publish_msgs = [initial_config()]

    return channel(
        description,
        "Adapter Link Management",
        sub_desc=subscribe_desc,
        sub_msgs=subscribe_msgs,
        pub_desc=publish_desc,
        pub_msgs=publish_msgs,
        tags=TAGS.ADAPTER_MSGS,
    )
