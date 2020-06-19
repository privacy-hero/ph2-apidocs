"""AsyncAPI Main Defintions.

Privacy Hero 2 - Websocket API - Adapter Diagnostic Message Definitions.

NOTES:
Internet Pause timed:
    Pause duration
    id - Just returned in the reply, ignored otherwise
    [List of device macs to pause]

VPN On-Off:
    URL - Optional - URL to establish VPN connection to.
    Method - VPN Method Openvpn / wireguard

"""

# from .util import mls
from .schemas import base_message, channel, Field
from .tags import TAGS


def device_info():
    """Send Device Information."""
    description = """
        This message is sent from the Adapter to the Backend whenever a new device
        is discovered, or if any of the data fields (excluding the online status)
        within this message about the device changes.  There is not difference between
        a new device or updating a pre-existing device.  Devices are identified by their
        MAC address and MAC is assumed to be unique on a single adapter.
    """

    tstamp_desc = """
        The time the device was discovered/changed.
    """

    mac_desc = """
        The Devices MAC address.  Assumed unique per adapter.  Eg. "00:11:22:33:44:55"
        Also accepts "001122334455" or "00-11-22-33-44-55"
    """

    ipv4_desc = """
        The IPv4 Address assigned to this Device. Alternatively, if the device is using
        a fixed IP and not one assigned by DHCP, the IP address it was discovered to be
        using.
    """

    ipv6_desc = """
        **Optional:** The IPv6 Address assigned to this Device. Alternatively, if the
        device is using a fixed IPv6 and not one assigned by DHCP, the IP address it was
        discovered to be using.
    """

    dhcp_hostname_desc = """
        The Hostname the Device declared itself as.  IF the device did not declare
        itself with a hostname, the adapter should synthesize a hostname for it.
        This hostname supplied to the backend should be fully qualified and include
        the local network suffix (if any) ie, the device declared itself as "MyPS5" and
        the local lan suffix is "lan" the hostname sent should be "MyPS5.lan"
    """

    dhcp_class_desc = """
        **Optional.** The class of device discovered from DHCP.  Can be omitted from
        the message if no class was provided by the device.
    """

    dhcp_clientid_desc = """
        **Optional.** The client id of device discovered from DHCP.  Can be omitted from
        the message if no client id was provided by the device.
    """

    upnp_desc = """
        **Optional.** IF a upnp xml device metadata can be retrieved from a device then
        it is to be gz compressed, base64-url encoded and sent in this field.  The
        maximum size of the ENCODED field may not exceed 120KB.  IF upnp data exists
        for a device, but it can not be sent because it would exceed the 120KB limit,
        then the field must be omitted and a message Logged to the backend stating how
        big the upnp payload was that could not be sent.  IF no upnp data can be
        obtained for a device, this field is omitted.
    """

    online_desc = """
        Current known Online state for the device.  This is the ONLY field whose change
        of value would not cause a new **"device info"** message to be sent.  If a
        device falls offline or comes back online, the **"device state"** message should
        be sent.
    """

    cmd = "device info"
    name = "DeviceInformation"
    title = "Device Information"
    summary = "Advise the Backend that the Device has been discovered or has changed."

    extra_fields = f"""
        {Field.mac(desc=mac_desc)},
        {Field.ipv4(desc=ipv4_desc)},
        {Field.ipv6(desc=ipv6_desc)},
        {Field.string("dhcp-hostname",dhcp_hostname_desc, minlength=1, maxlength=255)},
        {Field.string("dhcp-class", dhcp_class_desc)},
        {Field.string("dhcp-clientid", dhcp_clientid_desc)},
        {Field.binary("upnp.gz", upnp_desc)},
        {Field.boolean("online", online_desc)}
    """

    extra_example = """
        "mac"       : "00:11:22:33:44:55",
        "ipv4"      : "192.168.0.96",
        "ipv6"      : "::ffff:c0a8:60",
        "dhcp-hostname" : "MyPS5.lan",
        "online" : true
    """

    extra_required = '"tstamp", "mac", "ipv4", "dhcp-hostname", "online"'

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


DEVICE_SERVICES = [
    "ad-blocking",
    "device-protection",
    "internet-pause",
    "youtube-restricted",
    "safesearch",
]


def device_states():
    """Individual Device State Record."""
    service_desc = """
        The service/filter on the device which we wish to change the state of.
        - **ad-blocking** - Ad Blocking is Enabled on the device when True.
        - **device-protection** - Device Protection is Enabled on the device when True.
        - **internet-pause** - Internet is paused for the device when True.
        - **youtube-restricted** - Youtube returns restricted search results when True.
        - **safesearch** - Search Engines return "safe" results when True.

        Note: **internet-pause** also has a timed mode.  The boolean option in this
        message terminates any timed-pause current on the device and sets the state
        accordingly.
    """

    state_desc = """
        - **true** - The service/filter is enabled.
        - **false** - The service/filter is disabled.
    """

    fields = f"""
        {{
            {Field.enum("service",service_desc,DEVICE_SERVICES)},
            {Field.boolean("state", state_desc)}
        }}
    """

    return f"""
        {Field.object(None, "Service State", ["service","state"], fields)}
    """


def device_state_change():
    """Change Device State."""
    description = """
        This message is sent from the Backend to the adapter and instructs the adapter
        to make the listed state changes to the listed devices.  The message can
        contain multiple state changes, and multiple devices.  The devices listed are
        all triggered with the same state changes.
    """

    tstamp_desc = """
        The time the backend decided the state should change.  To be returned in the
        paired reply.
    """

    cmd = "device state change"
    name = "DeviceStateChange"
    title = "Device State Change"
    summary = "Advise the Adapter to change the state of the devices."

    id_desc = """
        **Optional**, ID Field.  The Adapter does not do any processing or verification
        of the ID field, if it is set, it must be returned verbatim in the paired reply.
    """

    devices_desc = """
        An array of Device MAC addresses the state changes are to be applied to.  All
        devices listed are to have the same state change made as listed in this message.
        Only after all devices states have been changed does the adapter send the paired
        reply.
    """

    mac_desc = """
        The Devices MAC address.  Assumed unique per adapter.  Eg. "00:11:22:33:44:55"
        Also accepts "001122334455" or "00-11-22-33-44-55"
    """

    states_desc = """
        The array of services and states to change.  If the service already has the
        requested state on the device no change is made but the reply includes this
        state.  If the service is not present in the states array, its state is not
        changed, and its current state is NOT returned to the paired reply.
    """

    extra_fields = f"""
        {Field.uuid("id", id_desc)},
        {Field.array("devices", devices_desc, Field.mac(None, mac_desc))},
        {Field.array("states", states_desc, device_states())}
    """

    extra_example = """
        "id"       : "85647580-68ec-44da-8bc8-3e7b8cf7b0e6",
        "devices" : ["53:CB:12:79:E5:F6","DD:0F:91:FE:9E:00","54:A4:33:F5:D8:A4"],
        "states" : [
            {"service": "ad-blocking", "state":false },
            {"service": "internet-pause", "state":false },
            {"service": "safe-search", "state":true }
        ]
    """

    extra_required = '"tstamp", "devices", "states"'

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


def device_discovery_channel():
    """Device Discovery messages."""
    description = """
        These are messages related to the discovery of new devices or changed
        devices.
    """

    subscribe_desc = "Device Discovery messages."
    subscribe_msgs = [device_info()]

    return channel(
        description,
        "Device Discovery",
        sub_desc=subscribe_desc,
        sub_msgs=subscribe_msgs,
        tags=TAGS.DEVICE_MSGS,
    )


def device_configuration_channel():
    """Device Configuration messages."""
    description = """
        These are messages related to the configuration of known devices.
    """

    # subscribe_desc = "Device Configuration messages."
    # subscribe_msgs = [device_info()]

    publish_desc = "Device Configuration messages."
    publish_msgs = [device_state_change()]

    return channel(
        description,
        "Device Configuration",
        pub_desc=publish_desc,
        pub_msgs=publish_msgs,
        tags=TAGS.DEVICE_MSGS,
    )
