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

    vpn_desc = f"""
        IF and ONLY IF this speedtest is through the VPN Tunnel, the URL/IP address of the
        VPN Server tested will be returned in the vpn field.  The backend will
        assume the speedtest result is for a WAN if this field is missing,
        therefore it is optional and must only be included in VPN Speedtest
        results. If the tunnel tested was a wireguard tunnel, this is the value
        from the *"server"* field in the servers vpn configuration.  And for
        strongSwan it is the *"right"* field in the servers vpn configuration.
        See {Xref.vpn_server_connect}.
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
        {Field.ipv4("ipv4", "The Connections Internet IPv4 Address")},
        {Field.ipv6("ipv6", "The Connections Internet IPv6 Address")},
        {Field.url("vpn", vpn_desc)}
    """
    extra_example = """
        "url": "http://www.3bb.com/speedtest",
        "location": "Phuket, Thailand",
        "provider": "3BB",
        "distance": -50,
        "rx": 185608437,
        "tx": 282140344,
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
    service_list = [
        "AdBlocking",
        "StreamRelocation",
        "Malware",
        "UPNP",
        "WIFI",
        "WPS",
        "Subscribed",
    ]

    service_state_desc = """
        An individual service state.
    """

    service_desc = f"""
        The name of the service being configured.
        - AdBlocking = Globally Enable/Disable AdBlocking
        - StreamRelocation = Globally Enable/Disabe Stream Relocation
        - UPNP = Enable a UPNP server to manage port forwarding for lan clients.
        - WIFI = Globally Enable/Disbale the Wifi on the Router.
        - WPS = Enable/Disable the WPS Button. This does not enable the WPS
          function, only allows the button to operate normally or not. Active
          WPS State changes are reported using the {Xref.wps_status} message
        - Subscribed = True - Normal Operation.  False - Subscription captive
          portal mode.  In captive portal mode only whitelisted domains have
          access to the internet. See {Xref.unsubscribed_whitelist} message.
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
                {"service": "AdBlocking", "state": true},
                {"service": "UPNP", "state": false},
                {"service": "WPS", "state": false},
                {"service": "Subscribed", "state": true}
            ]
        """
    else:
        cmd = "adapter-services-state"
        name = "AdapterServicesState"
        title = "Adapter Services State"
        summary = "Report current state of a service on the Adapter."

        description = f"""
            This is the reply to setting the adapter service states from the
            {Xref.adapter_services} message.
            \\
            If the configuration command contained multiple services, the reply
            may also contain multiple services, or services may be responded to
            in a group or individual, depending on how long the service takes to
            start on the adapter and the adapters implementation.  However, each
            reply must contain the tstamp from the original command from the
            backend, and the ID if present.
            \\
            This reply informs the backend of the final state of the service,
            ie, if UPNP server was commanded to turn on, but fails, the reply
            will be sent as a result of the failure AND will have its state set
            to false.  The tstamp will still reflect the tstamp in the original
            command, as will the ID if present.
            \\
            VPN status updates are not reported using this message. See the
            {Xref.vpn_connection_status} message for details.
            \\
            IF a service state can change without command from the backend, this
            message is sent unsolicited with the changed state for the service.
            in that case, the tstamp MUST be set to the tstamp of the time the
            state changed on the adapter, and there must be no ID field.
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


def vpn_server_strongswan_config():
    """Strongswan VPN Server Configuration."""
    cfg_desc = """
        The configuration for an individual strongswan server.
    """

    cfg_fields = f"""
    {{
        {Field.const_string("type","VPN Server Type","strongswan")},
        {Field.url("right",
        "Servers IP Address, may be an IPv4 or IPv6 address or a Server URL")},
        {Field.string("rightid","Servers ID")},
        {Field.string("rightsubnet","The servers subnet")},
        {Field.string("rightauth","The servers authentication protocol")},
        {Field.string("leftsourceip","Clients Source IP")},
        {Field.string("leftauth","The authentication protocol")},
        {Field.string("leftid","Clients ID")},
        {Field.string("secret","Authentication Credential")},
        {Field.int64("speed", "Current rated bandwidth for the tunnel.")},
        {Field.int64("latency", "Current rated latency for the tunnel.")}
    }}
    """

    cfg_required = ["type", "right", "rightid", "leftid", "secret"]

    return f"{{ {Field.object(None, cfg_desc, cfg_required, cfg_fields)} }}"


def vpn_server_wireguard_config():
    """Wireguard VPN Server Configuration."""
    cfg_desc = """
        The configuration for an individual wireguard server.
    """

    cfg_fields = f"""
    {{
        {Field.const_string("type","VPN Server Type","wireguard")},
        {Field.ip("server","Servers IP Address, may be IPv4 or IPv6")},
        {Field.port("port","Servers Port")},
        {Field.ipv4("ipv4","Clients IPV4 Address through the tunnel.")},
        {Field.ipv6("ipv6","Clients IPV6 Address through the tunnel.")},
        {Field.string("publickey","Public authentication key.", minlength=1)},
        {Field.string("privatekey","Private authentication key.", minlength=1)},
        {Field.int64("speed", "Current rated bandwidth for the tunnel.")},
        {Field.int64("latency", "Current rated latency for the tunnel.")}
    }}
    """

    cfg_required = ["type", "server", "port", "ipv4", "ipv6", "publickey", "privatekey"]

    return f"{{ {Field.object(None, cfg_desc, cfg_required, cfg_fields)} }}"


def vpn_connect():
    """Configure the VPN Servers the Router will communicate with."""
    cmd = "vpn-connect"
    name = "VPNConnect"
    title = "VPN Server Connect"
    summary = "Connect to a listed VPN Server."

    description = f"""
        This message causes the router to attempt to connect to one of the
        listed VPN servers.
        \\
        If there are untested servers in the list (servers without either the
        "speed" or "latency" fields in their configuration), the router will
        test them, and send the result back to the backend.  After testing is
        completed, the router will sort them, in order of fatest/lowest latency
        and then attempt to connect in that order.  Sorting is done as follows,
        the fastest server speed in the list is taken.  Of all servers that are
        within 10% of that speed, the one with the smallest latency is assumed
        to be the fastest.  The remaining servers are then sorted with the same
        rules, until no servers remain to be sorted.
        \\
        If there are no servers to be tested, then they are attempted to be
        connected in the order presented.
        \\
        IF the router has already established a VPN connection, AND the VPN
        server connected is present in the list (regardless of whether it has
        test data or not), then no reconnection will occur and it will not
        disconnect or attempt to reconnect as a result of receiving this
        message.  It will simply reply with the {Xref.vpn_connection_status}
        Message indicating the current server is connected.
        \\
        However, if the current VPN server connected IS NOT in the list, then
        the connection will be dropped and the list will be processed as if
        there was no connection to begin with.
        \\
        IF the server list is empty, and the VPN is connected, the Router will
        immediately drop the connection and report the connection is down using
        the {Xref.vpn_connection_status} message.
        \\
        This message is sent when a client requests the VPN connection be
        established, OR the Router has requested a {Xref.vpn_server_reconnect}.
        \\
        Because the router can ONLY rely on the credentials it was presented at
        the time the vpn-connect message was received, if for any reason the VPN
        tunnel disconnects, the router can try to immediately reconnect to the
        same tunnel with the same credentials.  If that fails, it can not use
        the credentials presented for any other tunnel as they may have expired
        or have been assigned to a different client.  In that case, the router
        can send a {Xref.vpn_server_reconnect} message to the backend to be
        provided with a fresh list of VPN servers and credentials with wish to
        re-establish VPN connection.  The backend will then reply with this
        {Xref.vpn_server_connect} message.
    """

    tstamp_desc = """
        The request timestamp of the configuration.
    """

    server_desc = """
        The message will contain a list of viable pre-selected servers.

        The highest priority entires (and therefore the first listed) will be
        those servers which require testing, in order of test priority.  There may be
        no servers of this type listed if there are no servers that REQUIRE
        testing.

        Following this will be a list of servers in priority order.  When
        connecting to the VPN, the router is to use this list and try to connect
        in the order presented.  IF the router is unable to establish a
        connection after trying all servers, it gives up attempting to connect.
    """

    extra_example = """
        "servers": [
        ]
    """

    extra_fields = f"""
        {Field.array("servers", server_desc, Field.one_of([vpn_server_wireguard_config(), vpn_server_strongswan_config()]) )}
    """

    extra_required = """
        "tstamp", "servers"
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


def vpn_reconnect():
    """Ask the Backend to reconnect the VPN and supply new server list/credentials."""
    cmd = "vpn-reconnect"
    name = "VPNReconnect"
    title = "VPN Server Reconnect"
    summary = "Reconnect to a listed VPN Server."

    description = f"""
        This message causes the backend to produce a new list of valid vpn
        servers and credentials and return it to the requesting router by way of
        a {Xref.vpn_server_connect} message.

        This message is only sent once, if an established VPN connection drops,
        and the Router is unable to re-establish a connection using the same
        credentials as the last dropped link.  IF the router is unable to
        establish a connection to any of the listed servers, the process
        terminates and this message is not sent.  Instead the router sends a
        {Xref.vpn_connection_status} message detailing the failure.
    """

    tstamp_desc = """
        The request timestamp of the configuration.
    """

    extra_example = None

    extra_fields = None

    extra_required = '"tstamp"'

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
    subscribe_msgs = [configure_service_state(reply=True), vpn_reconnect()]

    publish_desc = "Commands to set the Adapter Configuration."
    publish_msgs = [configure_service_state(), vpn_connect()]

    return channel(
        description,
        "Adapter Configuration",
        sub_desc=subscribe_desc,
        sub_msgs=subscribe_msgs,
        pub_desc=publish_desc,
        pub_msgs=publish_msgs,
        tags=TAGS.ADAPTER_MSGS,
    )
