"""AsyncAPI Main Defintions.

Privacy Hero 2 - Websocket API - Adapter Diagnostic Message Definitions.
"""

# from .util import mls
from .schemas import base_message, channel, Field, sha256_example, MsgDirection
from .adapter_diagnostics import log_level_field
from .tags import TAGS
from .xref import Xref

# ------------------------------------------------------------------------------


def link_established():
    """Adapter advice that the websocket link is established."""
    description = f"""
        This message is sent from the Adapter to the Backend as the very first
        message it sends AFTER establishing any websocket connection to the
        backend.  It allows the backend to perform link connection housekeeping
        for the adapter, which is necessary for proper operation.

        Upon receipt, the Backend will queue the initial configuration for the
        router in the following order:

        1. {Xref.initial_config}
        2. {Xref.unsubscribed_whitelist}
        3. {Xref.block_list} (1 message for each blocklist category)
        4. {Xref.adapter_services}
        5. {Xref.wifi_configuration}
        6. {Xref.vpn_set_bypass_domain}
        7. {Xref.vpn_server_connect}
        8. {Xref.streaming_auth}
        9. {Xref.streaming_cfg}
        10. {Xref.known_devices}
        11. {Xref.change_device_state} (As many as required to configure all devices)
        12. {Xref.set_bedtime} (1 message each for as many bedtime schedules exist.)
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
        id_field=False,
        direction=MsgDirection.RX_FROM_ROUTER,
    )


# ------------------------------------------------------------------------------


def initial_config():
    """Return Initial configuration of the adapter."""
    description = f"""
        This message contains the highest level configuration and is sent by the
        backend after a link is established, and the backend receives the
        {Xref.link_established} message from the Adapter.

        It may also be re-sent if any of the fields within it change, and the
        router needs to reconfigure itself upon receipt of the message.
    """

    tstamp_desc = """
        The tstamp in this message is the same tstamp sent in the *Link Established*
        message from the adapter which triggered it to be sent.
    """

    localtime_desc = """
        The IANA Timezone (see: https://www.iana.org/time-zones) of the routers
        localtime.  Only used by the router when it needs to calculate localtime
        offset back to UTC.  All internal timing inside the router and the vast
        majority of timestamps specified in messages are in UTC.  For Example
        "America/North_Dakota/New_Salem" or "Asia/Bangkok".
    """

    cmd = "initial cfg"
    name = "InitialConfig"
    title = "Initial Configuration"
    summary = "Initial Highest Level Configuration"

    extra_fields = f"""
        {Field.iana_tz("tz", localtime_desc)},
        {log_level_field(none_ok=True, name="loglevel",
         desc="The Minimum level of messages which should be logged to the backend.")}
    """
    extra_example = """
        "tz": "Africa/Casablanca",
        "loglevel": "DEBUG"
    """
    extra_required = """
        "tstamp",
        "version",
        "tz",
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
        id_field=False,
        direction=MsgDirection.TX_TO_ROUTER,
    )


# ------------------------------------------------------------------------------


def unsubscribed_whitelist():
    """Return the list of URLs which a user may access when unsubscribed."""
    description = f"""
        This message contains the list of urls devices may access when there is
        no active subscription for the router.  It is sent in response to a
        {Xref.link_established} message from the Adapter.
    """

    tstamp_desc = """
        The tstamp in this message is the same tstamp sent in the *Link Established*
        message from the adapter which triggered it to be sent.
    """

    whitelist_desc = f"""
        A list of regex url domains which, if matched, are allowed to be
        accessed even when the router is unsubscribed. All other HTTP traffic is
        routed to a url specified in the proxy field.

        I addition, all HTTPS traffic not to a whitelisted domain is simply blocked.

        This functionality is ONLY active if
        the {Xref.adapter_services} "Subscribed" service state is False.
    """

    proxy_desc = "The URL to route all non-whitelisted traffic to."

    cmd = "unsubscribed-whitelist"
    name = "UnsubscribedWhitelist"
    title = "Unsubscribed Whitelist"
    summary = "List of all urls that may be accessed when the router is not subscribed."

    extra_fields = f"""
        {Field.array("whitelist", whitelist_desc, Field.regex_url(None, "A URL Regex to match."))},
        {Field.url("proxy", proxy_desc )}
    """
    extra_example = r"""
        "whitelist" : [
            "^(.*\\.)?privacyhero.com$",
            "^.*\\.chargebee.com$"
        ]
    """
    extra_required = """
        "tstamp",
        "whitelist"
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
        id_field=False,
        direction=MsgDirection.TX_TO_ROUTER,
    )


# ------------------------------------------------------------------------------


def adapter_reset():
    """Trigger a hardware reset if the router."""
    description = f"""
        This message causes, after an optional delay, the router to be reset.
        {Xref.router_resetting} is sent in reply to this message before the reset
        occurs.
    """

    tstamp_desc = """
        The tstamp in this message is set by the Backend and must be returned
        verbatim in the reply.
    """

    in_desc = """
        The number of seconds to delay before resetting.  IF omitted, reset as
        fast as possible.
    """

    cmd = "reset"
    name = "Reset"
    title = "Router Reset"
    summary = "Cause Router to do a hardware reset."

    extra_fields = f"""
        {Field.timeout("in", in_desc)}
    """
    extra_example = """
        "in": 10
    """
    extra_required = """
        "tstamp"
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
        id_field=True,
        direction=MsgDirection.TX_TO_ROUTER,
    )


# ------------------------------------------------------------------------------


def adapter_resetting():
    """Advise that the adapter is about to reset."""
    description = f"""
        This message is sent as a reply to the {Xref.reset_router} message.
    """

    tstamp_desc = """
        The tstamp in this message is the same tstamp sent in the *Link Established*
        message from the adapter which triggered it to be sent.
    """

    in_desc = """
        The number of seconds before the reset will occur.  IF omitted, reset is
        imminent.
    """

    cmd = "resetting"
    name = "Resetting"
    title = "Router Resetting"
    summary = "Router is going to do a hardware reset."

    extra_fields = f"""
        {Field.timeout("in", in_desc)}
    """
    extra_example = """
        "in": 10
    """
    extra_required = """
        "tstamp"
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
        id_field=True,
        direction=MsgDirection.RX_FROM_ROUTER,
    )


# ------------------------------------------------------------------------------


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
    subscribe_msgs = [link_established(), adapter_resetting()]

    publish_desc = "Initial Configuration."
    publish_msgs = [initial_config(), adapter_reset(), unsubscribed_whitelist()]

    return channel(
        description,
        "Adapter Link Management",
        sub_desc=subscribe_desc,
        sub_msgs=subscribe_msgs,
        pub_desc=publish_desc,
        pub_msgs=publish_msgs,
        tags=TAGS.ADAPTER_MSGS,
    )
