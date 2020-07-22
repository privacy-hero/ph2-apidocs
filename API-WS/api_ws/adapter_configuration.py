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


def adapter_service_state():
    """Individual Service State Record."""
    service_list = ["VPN", "AdBlocking", "StreamRelocation", "Malware", "UPNP", "WIFI"]

    service_state_desc = """
        An individual service state.
    """

    service_desc = """
        The name of the service being configured.
    """

    state_desc = """
        The state to set the service to.
        * true = Turn the service ON.
        * false = Turn the service OFF.
    """

    service_state_fields = f"""
    {{
        {Field.enum("service", service_desc, service_list)},
        {Field.boolean("state", state_desc)}
    }}
    """

    return Field.object(
        None, service_state_desc, ["service", "state"], service_state_fields
    )


def configure_service_state(reply=False):
    """Configure the state of Adapter wide services."""
    if not reply:
        cmd = "adapter-services"
        name = "AdapterServices"
        title = "Adapter Services"
        summary = "Configure Adapter Level services on the Adapter."

        description = """
            This message causes the adapter that receives it to turn on/off the
            adapter wide services specified.  If any service is not specified, its
            state is not changed.

            IF the message contains multiple states, they may be replied to either
            individually or as a group.  In particular, "VPN" may take a long time
            to start.  "VPN" will not be replied to until the "VPN" has fully
            started or has failed.

            See the "vpn_status_update" message which allows progressive and
            detailed vpn startup/shutdown state to be reported to the Backend asynchronously.

            Regardless of the requested state, the reply for "VPN" always reflects
            the state which was achieved.  ie, if the VPN state in teh request was
            *true*, but the VPN failed to start, the reply must specify the actual
            state as *false*.  If other states may also fail to configure, they too
            must be replied with their actual state, and not the requested
            state.
            """

        services_desc = """
            A List of services and the states to set on the adapter.
        """

        tstamp_desc = """
            The request timestamp of the configuration, this tstamp must be returned
            in the reply with the results as the message tstamp.  In the
        """

        extra_example = """
            "services": [
                {"service": "VPN", "state": true},
                {"service": "AdBlocking", "state": true},
                {"service": "UPNP", "state": false}
            ]
        """
    else:
        cmd = "adapter-services-state"
        name = "AdapterServicesState"
        title = "Adapter Services State"
        summary = "Report current state of a service on the Adapter."

        description = """
            This is the reply to setting the adapter service states.

            If the configuration command contained multiple services, the reply
            may also contain multiple services, or services may be responded to
            in a group or individual, depending on how long the service takes to
            start on the adapter and the adapters implementation.  However, each reply
            must contain the tstamp from the original command from the backend.

            This reply informs the backend of the final state of the service,
            ie, if VPN was commanded to turn on, but fails, the reply will be
            sent as a result of the failure AND will have its state set to
            false.  The tstamp will still reflect the tstamp in the original command.

            See the "vpn_status_update" message which allows progressive and
            detailed vpn startup/shutdown state to be reported to the Backend asynchronously.

            IF a service state can change without command from the backend, this
            message is sent unsolicited with the changed state for the service.
            in that case, the tstamp MUST be set to the tstamp of the time the
            state changed on the adapter.
        """

        services_desc = """
            The final state of the service on the Adapter, after processing the
            command, or as a result of an asynchronous change.
        """

        tstamp_desc = """
            The response tstamp, as taken from the original command in the case
            of a reply, OR the tstamp the state changed on the adapter if sent asynchronously.
        """

        extra_example = """
            "services": [
                {"service": "AdBlocking", "state": true},
                {"service": "UPNP", "state": false}
            ]
        """

    extra_fields = f"""
        {Field.array("services", services_desc, adapter_service_state())}
    """

    extra_required = """
        "tstamp", "services"
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


def adapter_configuration_channel():
    """Adapter Config messages."""
    description = """
        These are messages related to the configuration of the adapter.

        These messages are sent on initial connection and also periodically as
        required to reflect user changes in the configuration.
    """

    subscribe_desc = "Configuration Acknowledgements from the Adapter"
    subscribe_msgs = [configure_service_state(reply=True)]

    publish_desc = "Commands to set the Adapter Configuration."
    publish_msgs = [configure_service_state()]

    return channel(
        description,
        "Adapter Configuration",
        sub_desc=subscribe_desc,
        sub_msgs=subscribe_msgs,
        pub_desc=publish_desc,
        pub_msgs=publish_msgs,
        tags=TAGS.ADAPTER_MSGS,
    )
