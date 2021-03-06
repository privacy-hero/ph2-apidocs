"""AsyncAPI Main Defintions.

Privacy Hero 2 - Websocket API - Streaming Configuration Message Definitions.
"""

# from .util import mls
from .schemas import base_message, channel, Field
from .tags import TAGS
from .xref import Xref

# -------------------------------------------------------------------------


def domain_proxy_cfg():
    """Domain Proxy Configuration."""
    cfg_desc = """
        The configuration for an individual proxy domain.
    """

    domain_match_object = f"""
    {{
        {Field.array("positive", "positive regex matches",
            items=Field.regex_url(None, "Individual positive regex url match" ))},
        {Field.array("negative", "negative regex matches",
            items=Field.regex_url(None, "Individual negative regex url match" ))}
    }}
    """

    cfg_fields = f"""
    {{
        {Field.string("name","Domain Descriptive Name")},
        {Field.object("match", "Regex domains to match against.",
            fields=domain_match_object, required=["positive","negative"])},
        {Field.array("servers", "List of Proxy Server URLs",
            items=Field.url(None, "Individual Proxy URL"))}
    }}
    """

    cfg_required = ["name", "match", "servers"]

    return f"{Field.object(None, cfg_desc, cfg_required, cfg_fields)}"


# -------------------------------------------------------------------------


def ip_proxy_cfg():
    """IP Proxy Configuration."""
    cfg_desc = """
        The configuration for an individual proxy IP Address.
    """

    cfg_fields = f"""
    {{
        {Field.ip("range","Net mask of the IP Address.")},
        {Field.array("servers", "List of Proxy Server IPs",
            items=Field.ip(None, "Individual Proxy IP"))}
    }}
    """

    cfg_required = ["range", "servers"]

    return f"{Field.object(None, cfg_desc, cfg_required, cfg_fields)}"


# -------------------------------------------------------------------------


def configure_streaming():
    """Configure the streaming configuration."""
    cmd = "cfg-streaming"
    name = "ConfigureStreaming"
    title = "Configure Streaming"
    summary = "Configure Router Streaming proxying."

    description = f"""
        This message causes the adapter to route all traffic in the specified
        wildcarded domains to the specified proxies.  And streaming service that
        is not configured for proxying is omitted from the message.  If there
        are no streaming services configured, the message will be sent with both
        the domain and ip lists empty.

        It will be sent initially following the router sending the
        {Xref.link_established} message to the backend.  And then periodically
        to track changes to streaming configuration as set by the client.
    """

    tstamp_desc = """
        The request timestamp of the configuration, this tstamp must be returned
        in the reply with the results as the message tstamp.
    """

    domain_desc = """
        Proxy domain url configuration.
    """

    ip_desc = """
        proxy ip address configuration.
    """

    extra_example = """
        "domains" : [],
        "ip-proxy" : []
    """

    extra_fields = f"""
        {Field.array("domains", domain_desc, domain_proxy_cfg(), minitems=0)},
        {Field.array("ip-proxy", ip_desc, ip_proxy_cfg(), minitems=0)}
    """

    extra_required = """
        "tstamp", "domains", "ip-proxy"
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


# -------------------------------------------------------------------------


def auth_streaming():
    """Send streaming credentials to the router."""
    cmd = "auth-streaming"
    name = "AuthorizeStreaming"
    title = "Authorize Streaming"
    summary = "Authorize the router to use the streaming proxy servers."

    description = f"""
        This message provides the credential needed by the streaming proxy
        server to authorize itself for streaming services.

        It will be sent initially following the router sending the
        {Xref.link_established} message to the backend.  Subsequently the
        message will be sent at approximately hourly intervals.  Each new
        credential supersedes the previous credential.
    """

    tstamp_desc = """
        The timestamp of the message.
    """

    extra_example = """
        "credential" : "e2d83939053740f1b80d84d09ed3c96b:1601543418:dGhpcyBpcyBub3QgYSBzaWduYXR1cmUuICBpdCBpcyBidXQgYW4gZXhhbXBsZS4gIFRoZSByZWFsIHNpZ25hdHVyZSBpcyBtdWNoIG11Y2ggbG9uZ2VyIGFzIGl0IGlzIGEgUlNBIFNpZ25hdHVyZSBvZiBhIFNIQTI1NiBIYXNoLg==",
        "expires" : 1601543418
    """

    extra_fields = f"""
        {Field.string("credential", "The credential to use to authenticate with the streaming proxy servers.")},
        {Field.unixepoch("expires", "When the credential may no longer be used.")}
    """

    extra_required = """
        "tstamp", "credential", "expires"
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


# -------------------------------------------------------------------------


def streaming_configuration_channel():
    """Streaming Config messages."""
    description = """
        These are messages related to the configuration of the streaming
        relocation service.

        These messages are sent on initial connection and also periodically as
        required to reflect user changes in the configuration.
    """

    # subscribe_desc = "Streaming Acknowledgements from the Router"
    # subscribe_msgs = []

    publish_desc = "Commands to set the Streaming Configuration."
    publish_msgs = [configure_streaming(), auth_streaming()]

    return channel(
        description,
        "Streaming Configuration",
        # sub_desc=subscribe_desc,
        # sub_msgs=subscribe_msgs,
        pub_desc=publish_desc,
        pub_msgs=publish_msgs,
        tags=TAGS.STREAMING_MSGS,
    )
