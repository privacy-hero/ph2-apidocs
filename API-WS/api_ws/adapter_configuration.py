"""AsyncAPI Main Defintions.

Privacy Hero 2 - Websocket API - Adapter Diagnostic Message Definitions.
"""

# from .util import mls
from .schemas import base_message, channel, Field
from .tags import TAGS
from .xref import Xref

# ------------------------------------------------------------------------------


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


# ------------------------------------------------------------------------------


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


# ------------------------------------------------------------------------------


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
        {Field.string("secret","Authentication Credential")}
    }}
    """

    cfg_required = ["type", "right", "rightid", "leftid", "secret"]

    return f"{{ {Field.object(None, cfg_desc, cfg_required, cfg_fields)} }}"


# ------------------------------------------------------------------------------


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
        {Field.string("privatekey","Private authentication key.", minlength=1)}
    }}
    """

    cfg_required = ["type", "server", "port", "ipv4", "ipv6", "publickey", "privatekey"]

    return f"{{ {Field.object(None, cfg_desc, cfg_required, cfg_fields)} }}"


# ------------------------------------------------------------------------------


def vpn_server_config():
    """Wireguard VPN Server Configuration."""
    cfg_desc = """
        The configuration for an individual VPN server.
        \\
        \\
        The **vpn_id** is to be used to report about status and speedtest results
        for the configured vpn tunnel.

        **speed** is the average speedtest TX result from the last months worth
        vpn speedtests on this server.  IF there is no **speed** field, the
        router is to create the **speed** value by connecting the tunnel and
        performing the speedtest.  The resulting TX speed in bytes per second of
        this one test becomes the **speed** for the purpose of selecting the
        fastest VPN Server.  Speed is selected as the TX value because most
        consumer internet connections are asynchronous, but have higher raw TX
        speed than RX, that means that any speedtest is more likely to max out
        RX than TX.

        **latency** is the average latency to the speedtest server from the last
        months worth of speedtest results on the server.  IF there is a missing
        latency result (ie, the speedtest reported -1)  then the latency value
        for the purpose of averaging is taken to be 1000ms which will force the
        latency to dis-favor links with unreliable connections.  The average is
        rounded to the nearest whole millisecond.

        **speed and latency** will either both be present, or neither present.
        If neither is present, the VPN tunnel is to be started and tested.

        The array will be pre-sorted in order from backend identified fastest
        server to slowest.  However, when the router must perform a speedtest to
        determine the vpn speed, it must resort.  The sorting algorithm works
        like this:

        ```
        Place all servers in an unsorted list of servers.
        Create a sorted list of servers which initally is empty.

        Of the servers in the list of unsorted servers, get the maximum speed
        value.
        Of the servers in the unsorted list whos speed is within 10% of the
        fastest speed in the list, remove the server with the lowest latency value
        and add it to the end of the list of sorted vpn servers.
        Repeat this selection process until there are no more servers in the
        unsorted server list.
        ```

        This algorithm will create a list of servers which trend from
        fastest/lowest latency down to slowest/highest latency.
    """

    vpn_server_cfg = f"""
    "config" : {{
        {Field.one_of(
            [vpn_server_wireguard_config(),
             vpn_server_strongswan_config()])}
    }}
    """

    speed_desc = """
        Current rated bandwidth for the tunnel in bytes per second.
    """

    latency_desc = """
        Current rated latency for the tunnel in milliseconds.
    """

    cfg_fields = f"""
    {{
        {Field.string("vpn_id", "Unique VPN ID")},
        {Field.int64("speed", speed_desc)},
        {Field.int64("latency", latency_desc)},
        {vpn_server_cfg}
    }}
    """
    #        {Field.object("config", "Server type specific configuration.", None,
    #                  vpn_server_cfg)}

    cfg_required = ["vpn_id"]

    return Field.object(None, cfg_desc, cfg_required, cfg_fields)


# ------------------------------------------------------------------------------


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
        and then attempt to connect in that order.
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
            {
                "vpn_id" : "wireguard-1",
                "speed" : 12345678,
                "latency" : 23,
                "config" : {
                    "type" : "wireguard",
                    "server" : "123.231.113.201",
                    "port" : "1234",
                    "ipv4" : "111.222.33.44",
                    "ipv6" : "87aa:5abf:2e90:574d:9dcc:cd2:af7b:fdfa",
                    "publickey" : "kjldfbghiuph",
                    "privatekey" : "skjdfbgkjqerbgkj"
                }
            },
            {
                "vpn_id" : "strongswan-1",
                "speed" : 12330000,
                "latency" : 27,
                "config" : {
                    "type" : "strongswan",
                    "right" : "123.231.113.201",
                    "rightid" : "serverid",
                    "leftid" : "client1",
                    "secret" : "kjldfbghiuph"
                }
            }
        ]
    """

    extra_fields = f"""
        {Field.array("servers", server_desc, vpn_server_config() )}
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


# ------------------------------------------------------------------------------


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


# ------------------------------------------------------------------------------


def vpn_status():
    """Advises the Backend of the current status of the VPN connection."""
    cmd = "vpn-status"
    name = "VPNStatus"
    title = "VPN Connection Status"
    summary = "Report VPN Connection Status."

    description = f"""
        This message advises the current VPN status to the backend.

        During VPN connection, multiple status messages should be sent tracking
        the major phases of VPN connection initiation, and also, reconnections
        on a failed link and link disconnection.  VPN Connection/Disconnection
        is triggered by the receipt of a {Xref.vpn_server_connect} message.
    """

    tstamp_desc = """
        The request timestamp of the configuration.
    """

    status_desc = f"""
    The current status of the VPN process.

    - *test-connecting* = Connecting to a VPN server to test.
    - *testing* = Test connection to VPN succeeded and test started.  Test
      results will be sent in {Xref.speedtest_result}.
    - *test-failed* = Either the connection couldn't be established to test, or
      the test has failed to execute.
    - *connecting* = Connecting the VPN tunnel for general use.
    - *connected* = The connection to the VPN is established and routing is
      operational.
    - *failed* = The vpn server failed to connect or the link broke.   After
      this call the router may no longer use the credentials presented in
      {Xref.vpn_server_connect} for the server.
    - *reconnecting* = The VPN server was running and failed, trying to
      reconnect. This status is sent instead of the *connecting* status when a
      vpn link was established, but dropped and we are attempting to
      re-establish the connection.
    - *disconnected* = The last possible server was tested and failed, giving up
      trying to enable VPN.  *server* should not be present, as no server is
      being accessed in this state.
    """

    desc_string = """
    String description providing extra information about a state.
    It is valid for the same state to be sent multiple times with changing desc_string.

    For example *testing* multiple times for the same URL with a running commentary
    about the test as it executes.
    """

    extra_fields = f"""
        {Field.enum("status", status_desc,
        ["test-connecting", "testing","test-failed", "connecting", "connected",
        "failed", "reconnecting", "disconnected"])},
        {Field.string("server", "The server ID, sent for every status except *disconnected*")},
        {Field.string("description", desc_string)}
    """

    extra_required = '"tstamp","status"'
    extra_example = """
        "status" : "testing",
        "server" : "wireguard-1",
        "description" : "TX Speedtest started"
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


def adapter_configuration_channel():
    """Adapter Config messages."""
    description = """
        These are messages related to the configuration of the adapter.

        These messages are sent on initial connection and also periodically as
        required to reflect user changes in the configuration.
    """

    subscribe_desc = "Configuration Acknowledgements from the Adapter"
    subscribe_msgs = [
        configure_service_state(reply=True),
        vpn_reconnect(),
        vpn_status(),
        wps_status(),
    ]

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
