"""AsyncAPI Main Defintions.

Privacy Hero 2 - Websocket API - Adapter Diagnostic Message Definitions.
"""

# from .util import mls
from .schemas import base_message, channel, Field
from .tags import TAGS


def log_level_field(none_ok=True, name="level", desc="The level of the log messages."):
    """Return log level field."""
    levels = []
    if none_ok:
        levels.append("NONE")
    levels += ["ERROR", "WARNING", "DEBUG"]

    return Field.enum(name, desc, levels)


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

    distance_desc = """
        The distance is the approximate distance from the adapter to the speedtest
        server.  The distance can be either a value that is estimated to be LESS THAN
        the distance stated, or CLOSE TO the distance stated.

        * -VE = The estimate is a LESS THAN this estimate.
        * +VE = The estimate is a CLOSE TO this estimate.

        The distance is measured in whole MILES.
    """

    ping_desc = """
        The ping result is an array with a minimum of 10 entries, that represent
        the results from at least 10 consecutive pings to the server.
        The ping result is a positive integer which represents the number of
        whole milliseconds (rounded up) it took for the ping to the server to
        be replied to.

        IF a ping fails, the position in the array where the result would be is set
        to null.

        There can be more than 10 results, but there can not be less than 10.
    """

    connection_desc = """
        The connection which was tested.

        * **WAN** is the native WAN Interface of the Adapter.
        * **VPN** is the through the VPN tunnel.
    """

    cmd = "speedtest"
    name = "SpeedTest"
    title = "Speed Test"
    summary = "Report of Speed Test Results"

    extra_fields = f"""
        {Field.url("url",
            "The URL of the website the speedtest was conducted against.")},
        {Field.string("location",
            "The String description of the speedtest server location")},
        {Field.string("provider",
            "The name of the ISP/Network operator managing the speedtest server.")},
        {Field.int64("distance", distance_desc)},
        {Field.int("rx", "Result in bits per second of the receive speed test.")},
        {Field.int("tx", "Result in bits per second of the transmit speed test.")},
        {Field.enum("connection",connection_desc, ["WAN","VPN"])},
        {Field.ipv4("ipv4", "The Connections Internet IPv4 Address")},
        {Field.ipv6("ipv6", "The Connections Internet IPv6 Address")}
    """
    extra_example = """
        "url": "http://www.3bb.com/speedtest",
        "location": "Phuket, Thailand",
        "provider": "3BB",
        "distance": -50,
        "rx": 185608437,
        "tx": 282140344,
        "connection": "WAN",
        "ipv4": "183.89.198.67"
    """
    extra_required = """
        "tstamp",
        "url",
        "location",
        "provider",
        "distance",
        "rx",
        "tx",
        "connection",
        "ipv4"
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

    url_desc = """
        OPTIONAL: URL to perform the speedtest against.  IF not supplied use
        the best url probed from speedtest server lists.
    """

    connection_desc = """
        OPTIONAL: The connection to test.  If not present, the test is to be preformed
        against the native WAN interface.

        * **WAN** is the native WAN Interface of the Adapter.
        * **VPN** is the through the VPN tunnel.
    """

    cmd = "run-speedtest"
    name = "RunSpeedTest"
    title = "Run Speed Test"
    summary = "Run a Speed Test and Report the Results"

    extra_fields = f"""
        {Field.enum("connection",connection_desc, ["WAN","VPN"])},
        {Field.url("url", url_desc)}
    """

    extra_example = """
        "connection": "VPN",
        "url": "http://www.3bb.com/speedtest"
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
        TAGS.ADAPTER_DIAGS,
        tstamp_desc,
        extra_fields,
        extra_example,
        extra_required,
    )


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
