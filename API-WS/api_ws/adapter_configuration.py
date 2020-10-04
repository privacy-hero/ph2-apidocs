"""AsyncAPI Main Defintions.

Privacy Hero 2 - Websocket API - Adapter Configuration Message Definitions.
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
