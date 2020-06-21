"""AsyncAPI Main Defintions.

Privacy Hero 2 - Websocket API - Device Discovery Message Definitions.

NOTES:
Internet Pause timed:
    Pause duration
    id - Just returned in the reply, ignored otherwise
    [List of device macs to pause]

VPN On-Off: (This should be for adapter.  Device is just on/off)
    URL - Optional - URL to establish VPN connection to.
    Method - VPN Method Openvpn / wireguard

"""

# from .util import mls
from .schemas import base_message, channel, Field, sha256_example
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


def known_devices():
    """Known Devices message.

    Sent from Backend to Adapter after successful connection.
    """
    description = """
        This message is sent by the Backend after initial adapter configuration
        upon successful connection of an adapter to the backend.  It tells the adapter
        all devices known by the backend.  If a device is not in this list of devices
        that the adapter knows about, and the device is currently offline, the device
        is deleted. If the device is Online, a new Device Info for the device is queued
        to the backend to update the backends knowledge of all the connected devices.
        IF any of the known device data differs to the data the adapter knows about
        the device, a new device info message is queued to update the backends knowledge
        of the device.
    """

    tstamp_desc = """
        The time the device was discovered/changed.
    """

    mac_desc = """
        The Devices MAC address."""

    ipv4_desc = """
        The IPv4 Address assigned to this Device."""

    ipv6_desc = """
        **Optional:** The IPv6 Address assigned to this Device."""

    dhcp_hostname_desc = """
        The Hostname the Device declared itself as."""

    dhcp_class_desc = """
        **Optional.** The class of device discovered from DHCP."""

    dhcp_clientid_desc = """
        **Optional.** The client id of device discovered from DHCP."""

    upnp_desc = """
        **Optional.** IF a upnp xml device metadata record has been sent to
        the backend for the device, this field will contain the sha256 (base64 encoded)
        hash of the xml metadata file, so that the adapter can confirm the metadata
        held by the backend is accurate.  If it is not accurate, a device info message
        with the correct data is queued for the device.
    """

    online_desc = """
        The current Online state the backend believes is valid for the device.  IF it
        is not valid, a device info message is not sent to the backend to correct it,
        but a "Device State Changed" message is.
    """

    devices_desc = """
        An array of all devices known by the backend for the adapter.
    """

    cmd = "known devices"
    name = "KnownDevices"
    title = "Known Device Information"
    summary = "Configures the Adapter with all devices known by the backend."

    device_fields = f"""
    {{

        {Field.mac(desc=mac_desc)},
        {Field.ipv4(desc=ipv4_desc)},
        {Field.ipv6(desc=ipv6_desc)},
        {Field.string("dhcp-hostname",dhcp_hostname_desc, minlength=1, maxlength=255)},
        {Field.string("dhcp-class", dhcp_class_desc)},
        {Field.string("dhcp-clientid", dhcp_clientid_desc)},
        {Field.sha256("upnp.csum", upnp_desc)},
        {Field.boolean("online", online_desc)}
    }}
    """

    extra_fields = f"""
        {Field.array("devices", devices_desc,
            Field.object(None, "Device Info",
                ["mac", "ipv4", "dhcp-hostname", "online"],
                device_fields))}
    """

    extra_example = f"""
        "devices" : [
            {{
                "mac"       : "00:11:22:33:44:55",
                "ipv4"      : "192.168.0.96",
                "ipv6"      : "::ffff:c0a8:60",
                "dhcp-hostname" : "MyPS5.lan",
                "online" : true
            }},
            {{
                "mac"       : "26:C7:71:4C:97:37",
                "ipv4"      : "192.168.0.18",
                "ipv6"      : "::ffff:c0a8:12",
                "dhcp-hostname" : "OnkyoAmp.lan",
                "upnp.csum" : "{sha256_example("UPNP XML Example")}",
                "online" : true
            }}
        ]
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


def device_discovery_channel():
    """Device Discovery messages."""
    description = """
        These are messages related to the discovery of new devices or changed
        devices.
    """

    subscribe_desc = "Device Discovery messages."
    subscribe_msgs = [device_info()]
    publish_msgs = [known_devices()]

    return channel(
        description,
        "Device Discovery",
        pub_desc=subscribe_desc,
        pub_msgs=publish_msgs,
        sub_desc=subscribe_desc,
        sub_msgs=subscribe_msgs,
        tags=TAGS.DEVICE_MSGS,
    )
