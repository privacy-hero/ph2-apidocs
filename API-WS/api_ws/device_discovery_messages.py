"""AsyncAPI Main Defintions.

Privacy Hero 2 - Websocket API - Device Discovery Message Definitions.

NOTES:
Internet Pause timed:
    Pause duration
    id - Just returned in the reply, ignored otherwise
    [List of device macs to pause]

VPN On-Off: (This should be for adapter.  Device is just on/off)
    URL - Optional - URL to establish VPN connection to.
    Method - VPN Method Openvpn / wireguard,

"""

# from .util import mls
from .schemas import base_message, channel, Field
from .tags import TAGS
from .xref import Xref


def dhcp_device_info(desc):
    """Return the fields we want from dhcp about the device."""
    # If want the required list, just return the list of required fields.
    required = ["hostname"]

    dhcp_hostname_desc = """
        The Hostname the Device declared itself as.  IF the device did not declare
        itself with a hostname, the adapter should synthesize a hostname for it.
        This hostname supplied to the backend should be the hostname only part
        and not include the network suffix. ie, if the device declared itself as
        "MyPS5" and the local lan suffix is "lan" the hostname sent should be
        "MyPS5".  This is Option 12 from the DHCP Request.

    """

    dhcp_class_desc = """
        **Optional.** The class of device discovered from DHCP.  Can be omitted from
        the message if no class was provided by the device.  This is option 60
        from the DHCP Request.

    """

    dhcp_clientid_desc = """
        **Optional.** The client id of device discovered from DHCP.  Can be omitted from
        the message if no client id was provided by the device. This is option
        61 from the DHCP Request.
    """

    dhcp_parameter_list = """
        **Optional.** The Parameter list the client requested be returned to
        it's dhcp request.  This is option 55 from the DHCP Request.
    """

    fields = f"""
        {{
            {Field.string("hostname",dhcp_hostname_desc, minlength=1, maxlength=255)},
            {Field.string("class", dhcp_class_desc)},
            {Field.string("clientid", dhcp_clientid_desc)},
            {Field.string("parameters", dhcp_parameter_list)}
        }}
    """

    return f"""
        {Field.object("dhcp", desc, required, fields, additional=True)}
    """


def upnp_device_info(desc):
    """Return the fields we want from upnp about the device."""
    device_type_desc = """
        The Device type reported by the UPNP Data of this internal device.
        *eg: urn:schemas-upnp-org:device:InternetGatewayDevice:1*
    """

    manufacturer_desc = """
        The Device manufacturer reported by the UPNP Data of this internal device.
        *eg: Samsung*
    """

    model_name_desc = """
        The Model Name reported by the UPNP Data of this internal device.
        *eg: QN82Q80RAFXZA*
    """

    friendly_name_desc = """
        The Friendly Name reported by the UPNP Data of this internal device.
        *eg: 80" 4k QLED Flatscreen TV*
    """

    service_desc = """
        The List of service types reported by the UPNP Data of this internal
        device.
        *eg: ["urn:schemas-upnp-org:service:Layer3Forwarding:1"]*
    """

    fields = f"""
        {{
            {Field.string("deviceType", device_type_desc)},
            {Field.string("manufacturer", manufacturer_desc)},
            {Field.string("modelName", model_name_desc)},
            {Field.string("friendlyName", friendly_name_desc)},
            {Field.array("serviceTypeList", service_desc,
                Field.string(None, "Individual Service Type Entry"))}
        }}
    """

    array_items = f"""
        {Field.object(None, "UPNP Device Description", ["deviceType"],
            fields, additional=True)}
    """

    return f"""
        {Field.array("upnp", desc, array_items)}
    """


def smb_device_info(desc):
    """Return the fields we want from upnp about the device."""
    # If want the required list, just return the list of required fields.
    required = ["name"]

    smb_name_desc = """
        If the SMB/Netbios reported Name of the device can be determined, it is
        sent in this field.
    """

    smb_domain_desc = """
        If the SMB/Netbios reported Domain of the device can be determined, it is
        sent in this field.
    """

    fields = f"""
    {{
        {Field.string("name", smb_name_desc)},
        {Field.string("domain", smb_domain_desc)}
    }}
    """

    return f"""
        {Field.object("smb", desc, required, fields, additional=True)}
    """


def snmp_device_info(desc):
    """Return the fields we want from snmp about the device."""
    # If want the required list, just return the list of required fields.
    required = ["sysoid"]

    sysoid_desc = """
        The System OID of the Device.
    """

    name_desc = """
        The name the device reports via snmp.
    """

    description_desc = """
        The description the device reports via snmp.
    """

    contact_desc = """
        The contact the device reports via snmp.
    """

    location_desc = """
        The location the device reports via snmp.
    """

    field = f"""
    {{
        {Field.string("sysoid", sysoid_desc)},
        {Field.string("name", name_desc)},
        {Field.string("description", description_desc)},
        {Field.string("contact", contact_desc)},
        {Field.string("location", location_desc)}
    }}
    """

    return f"""
        {Field.object("snmp", desc, required, field, additional=True)}
    """


def hua_device_info(desc):
    """Return the fields we want from the devices host user agent about the device."""
    hua_desc = """
        This is the host user agent sniffed from http traffic from the device.
        This data can not be obtained from https, only http connections.  As
        there may be more than one userAgent string detected, this is a list of
        the detected useragents.
    """

    fields = f"""
        {{
            {Field.string("userAgent", hua_desc)}
        }}
    """

    items = f"""
        {Field.object(None, "HTTP User Agent List", ["userAgent"],
            fields, additional=True)}
    """

    return f"""
        {Field.array("hua", desc, items)}
    """


def bonjour_device_info(desc):
    """Return the fields we want from the devices bonjour probes."""
    name_desc = """
        The name of a device discovered via Bonjour.
    """

    service_desc = """
        The list of services exposed via Bonjour.
    """

    service_name_desc = """
        The name of a service discovered on the device via Bonjour.
    """

    service_txt_desc = """
        The TXT record from Answers or Additional records.
    """

    service_fields = f"""
        {{
            {Field.string("name",service_name_desc)},
            {Field.array("txt", service_txt_desc, items=
                Field.string(None, service_txt_desc))}
        }}
    """

    fields = f"""
        {{
            {Field.string("name", name_desc)},
            {Field.array("services", service_desc, items=
                Field.object(None,service_desc,["name"],
                            fields=service_fields, additional=True))}
        }}
    """

    return f"""
        {Field.object("bonjour", desc, ["name"], fields, additional=True)}
    """


def device_info():
    """Send Device Information."""
    description = """
        This message is sent from the Adapter to the Backend whenever a new device
        is discovered, or if any of the data fields (excluding the online status)
        within this message about the device changes.  There is no difference between
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

    dhcp_desc = """
        DHCP Data discovered about the device.
    """

    upnp_desc = """
        **Optional.** IF a upnp xml device metadata can be retrieved from a device then
        it is to be sent in this sub field, otherwise it is omitted.  It is
        possible for a single physical device to report as multiple internal
        upnp devices.  Each discovered internal upnp device is reported in this array.
    """

    smb_desc = """
        **Optional.** If SMB/Netbios metadata can be obtained/probed for a device,
        it is sent in this field, otherwise it is omitted.
    """

    snmp_desc = """
        **Optional.** If SNMP metadata can be obtained/probed for a device,
        it is sent in this field, otherwise it is omitted.
    """

    bonjour_desc = """
        **Optional.** If BONJOUR metadata can be obtained/probed for a device,
        it is sent in this field, otherwise it is omitted.
    """

    hua_desc = """
        **Optional.** HTTP User Agents discovered for the device, otherwise
        it is omitted.
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

    meta_fields = f"""
    {{
        {dhcp_device_info(dhcp_desc)},
        {upnp_device_info(upnp_desc)},
        {snmp_device_info(snmp_desc)},
        {bonjour_device_info(bonjour_desc)},
        {smb_device_info(smb_desc)},
        {hua_device_info(hua_desc)}
    }}
    """

    extra_fields = f"""
        {Field.mac(desc=mac_desc)},
        {Field.ipv4(desc=ipv4_desc)},
        {Field.ipv6(desc=ipv6_desc)},
        {Field.boolean("online", online_desc)},

        {Field.object("meta", "metadata discovered about the device.",
            fields=meta_fields, additional=True)}
    """

    extra_example = """
        "mac"       : "00:11:22:33:44:55",
        "ipv4"      : "192.168.0.96",
        "ipv6"      : "::ffff:c0a8:60",
        "meta"      : {
            "dhcp"      : {
            "hostname"  : "MyPS5"
            }
        },
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

    def flag_desc(name):
        return f"""
            {name} Metadata already recorded about the device.
            Default to *false* if not present.
        """

    description = f"""
        This message is sent by the Backend after initial adapter configuration
        upon successful connection of an adapter to the backend (after receipt
        of the {Xref.link_established}) message.  It tells the adapter all
        devices known by the backend.  If a device is not in this list of
        devices that the adapter knows about, and the device is currently
        offline, the device is deleted. If the device is Online, a new Device
        Info for the device is queued to the backend to update the backends
        knowledge of all the connected devices.  IF any of the known device data
        differs to the data the adapter knows about the device, a new device
        info message is queued to update the backends knowledge of the device.
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

    hostname_desc = """
        The Hostname to use for the device (overrides the devices self declared
        hostname *option 12 from the dhcp request*).
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
        {Field.string("user-hostname", hostname_desc, minlength=1, maxlength=255)},
        {Field.boolean("online", online_desc)},
        {Field.boolean("dhcp", flag_desc("DHCP"))},
        {Field.boolean("upnp", flag_desc("UPNP"))},
        {Field.boolean("snmp", flag_desc("SNMP"))},
        {Field.boolean("bonjour", flag_desc("BONJOUR"))},
        {Field.boolean("smb", flag_desc("SMB/Netbios"))},
        {Field.boolean("hua", flag_desc("HTTP User Agent"))}
    }}
    """

    extra_fields = f"""
        {Field.array("devices", devices_desc,
            Field.object(None, "Device Info",
                ["mac", "ipv4", "dhcp-hostname", "online"],
                device_fields, additional=True))}
    """

    extra_example = """
        "devices" : [
            {
                "mac"       : "00:11:22:33:44:55",
                "ipv4"      : "192.168.0.96",
                "ipv6"      : "::ffff:c0a8:60",
                "user-hostname"  : "PS5-Lounge",
                "online"    : true,
                "dhcp"      : true
            },
            {
                "mac"       : "26:C7:71:4C:97:37",
                "ipv4"      : "192.168.0.18",
                "ipv6"      : "::ffff:c0a8:12",
                "user-hostname"  : "OnkyoAmp",
                "online"    : true,
                "dhcp"      : true,
                "upnp"      : true
            }
        ]
    """

    extra_required = '"tstamp", "mac", "ipv4", "online"'

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
