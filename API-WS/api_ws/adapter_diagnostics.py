"""AsyncAPI Main Defintions.

Privacy Hero 2 - Websocket API - Adapter Diagnostic Message Definitions.
"""

# from .util import mls
from .schemas import base_message, channel, Field
from .tags import TAGS
from .xref import Xref


def log_level_field(none_ok=True, name="level", desc="The level of the log messages."):
    """Return log level field."""
    levels = []
    if none_ok:
        levels.append("NONE")
    levels += ["ERROR", "WARNING", "DEBUG"]

    return Field.enum(name, desc, levels)


# ------------------------------------------------------------------------------


def adapter_log():
    """Return Adapter Message Log Message."""
    description = """
        This message causes the backend to log error and general diagnostic messages
        from the adapter to the system logs.  It can be sent anytime the adapter
        wishes to log a message.
        """

    tstamp_desc = """
        The time the log message was generated inside the adapter. (According to the
        adapters internal clock.)
    """

    cmd = "log"
    name = "LogMsg"
    title = "Log Message"
    summary = "Log Message to Backend"

    extra_fields = f"""
        {log_level_field(none_ok=False)},
        {Field.string("log","The message to be logged by the Adapter.", minlength=1)}
    """
    extra_example = '"level" : "ERROR", "log" : "An Error ocurred inside the Adapter"'
    extra_required = '"tstamp", "level", "log"'

    return base_message(
        cmd,
        name,
        title,
        summary,
        description,
        TAGS.ADAPTER_DIAGS,
        tstamp_desc,
        extra_fields,
        extra_example,
        extra_required,
    )


# ------------------------------------------------------------------------------


def adapter_speedtest_result_oneway(name: str) -> str:
    """Speedtest result for a single direction."""
    speedtest_desc = """The result of the speedtest in the specified direction."""

    speedtest_fields = f"""
    {{
        {Field.int64("txfr", desc="The total number of bytes transferred.")},
        {Field.int64("ms", desc="The total number of milliseconds the transfer took.")}
    }}
    """

    return Field.object(name, speedtest_desc, ["txfr", "ms"], speedtest_fields)


# ------------------------------------------------------------------------------


def adapter_speedtest_results():
    """Return the last speedtest result to the Backend."""
    description = """
        This message causes the latest speedtest result to be logged for the
        Adapter in the backend.
        """

    tstamp_desc = """
        IF the speedtest was performed as a result of a automatic or scheduled test
        the timestamp is the time the speed test started on the adapter.

        IF the speedtest was conducted as a result of a command from the backend,
        the tstamp is the tstamp from the backend request to commence the speedtest.
    """

    vpn_desc = f"""
        IF and ONLY IF this speedtest is through the VPN Tunnel, the VPN ID of the
        VPN Server tested will be returned in the vpn field.  The backend will
        assume the speedtest result is for a WAN if this field is missing,
        therefore it is optional and must only be included in VPN Speedtest
        results. See {Xref.vpn_server_connect}.
    """

    cmd = "speedtest"
    name = "SpeedTest"
    title = "Speed Test"
    summary = "Report of Speed Test Results"

    extra_fields = f"""
        {Field.ip("address",
            "The IP of the website the speedtest was conducted against.")},
        {Field.ipv4("ipv4", "The Connections Internet IPv4 Address")},
        {Field.ipv6("ipv6", "The Connections Internet IPv6 Address")},
        {Field.url("vpn", vpn_desc)},
        {adapter_speedtest_result_oneway("tx")},
        {adapter_speedtest_result_oneway("rx")},
        {Field.array("latency",
            "Results of latency test on speedtest server, for a minimum of 10 tests.",
            items=Field.int64(None, "Ping latency in ms, -1 for no reply."),
            minitems=10)}
    """

    extra_example = """
        "ip": "107.180.77.130",
        "ipv4": "183.89.198.67",
        "rx": {
            "txfr": 445173760,
            "ms": 30382
        },
        "tx": {
            "txfr": 11636736,
            "ms": 30222
        },
        "latency": [25, 22, 27, -1, 19, -1, 26, 27, 25, 25]
    """
    extra_required = """
        "tstamp",
        "address",
        "ipv4",
        "rx",
        "tx",
        "latency"
    """

    return base_message(
        cmd,
        name,
        title,
        summary,
        description,
        TAGS.ADAPTER_DIAGS,
        tstamp_desc,
        extra_fields,
        extra_example,
        extra_required,
    )


# ------------------------------------------------------------------------------


def run_speedtest():
    """Return the command to trigger an adapter to perform a speedtest.."""
    description = """
        This message causes the adapter that receives it to perfrom ping and speedtests
        and return the results in a "speedtest" message.
        """

    tstamp_desc = """
        The request timestamp of the speedtest, this tstamp must be returned
        in the reply with the results as the message tstamp.
    """

    connection_desc = """
        The connection to test.

        * **WAN** is the native WAN Interface of the Adapter.
        * **VPN** is the through the VPN tunnel.
    """

    ip_desc = """
        OPTIONAL, if present perform speedtest against the provided servers ip
        address and not the one presented in configuration.
    """

    cmd = "run-speedtest"
    name = "RunSpeedTest"
    title = "Run Speed Test"
    summary = "Run a Speed Test and Report the Results"

    extra_fields = f"""
        {Field.enum("connection",connection_desc, ["WAN","VPN"])},
        {Field.url("ip", ip_desc)}
    """

    extra_example = """
        "connection": "WAN",
        "ip": "107.180.77.130"
    """
    extra_required = """
        "tstamp",
        "connection"
    """

    return base_message(
        cmd,
        name,
        title,
        summary,
        description,
        TAGS.ADAPTER_DIAGS,
        tstamp_desc,
        extra_fields,
        extra_example,
        extra_required,
    )


# ------------------------------------------------------------------------------


def adapter_diagnostics_channel():
    """Adapter Diagnostic messages."""
    description = """
        These are messages related to the diagnostic processes of the adapter.

        Diagnostics are performed as required by the adapter, and also as a result of
        explicit command from the backend.

        If the adapter requested a diagnostic check, the tstamp in the reply MUST match
        the tstamp in the request.
    """

    subscribe_desc = "Diagnostic reports from the Adapter."
    subscribe_msgs = [adapter_log()]

    return channel(
        description,
        "Adapter Diagnostics",
        sub_desc=subscribe_desc,
        sub_msgs=subscribe_msgs,
        tags=TAGS.ADAPTER_DIAGS,
    )


# ------------------------------------------------------------------------------


def speedtest_channel():
    """Speedtest messages."""
    description = """
        These are messages related to the diagnostic processes of the adapter.

        Diagnostics are performed as required by the adapter, and also as a result of
        explicit command from the backend.

        If the adapter requested a diagnostic check, the tstamp in the reply MUST match
        the tstamp in the request.
    """

    subscribe_desc = "Speedtest Reports from the Adapter."
    subscribe_msgs = [adapter_speedtest_results()]

    publish_desc = "Commands to instigate speedtest checks."
    publish_msgs = [run_speedtest()]

    return channel(
        description,
        "Speed Test",
        sub_desc=subscribe_desc,
        sub_msgs=subscribe_msgs,
        pub_desc=publish_desc,
        pub_msgs=publish_msgs,
        tags=TAGS.ADAPTER_DIAGS,
    )
