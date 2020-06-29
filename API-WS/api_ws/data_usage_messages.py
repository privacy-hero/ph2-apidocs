"""AsyncAPI Main Defintions.

Privacy Hero 2 - Websocket API - Adapter/Device Data Usage Reporting.
"""

# from .util import mls
from .schemas import base_message, channel, Field
from .tags import TAGS


def data_usage():
    """Adapter/Device Data Usage Reporting."""
    description = """
        This message is sent from the Adapter to the Backend every hour and is
        synchronized to the top of each hour.  It reports the data usage for
        both the Adapter as a whole, and each ACTIVE device within that hour.

        In order to prevent spikes of data hitting the backend at the end of
        every hour, this message should be delayed to be sent for a random
        interval up to 10 minutes, after the end of each hour.  However, the
        tstamp field should reflect the hour that is being reported, and NOT the
        time the message was actually sent.
    """

    tstamp_desc = """
        The time of the Adapter/Device Data Usage Report, this should be
        synchronized to the top of each hour.
    """

    adapter_tx_desc = """
        This is the total number of bytes sent by the Adapter to the internet in
        the hour.
    """

    adapter_rx_desc = """
        This is the total number of bytes received by the Adapter from the internet in
        the hour.
    """

    devices_desc = """
        The list of all devices which were active during the hour and
        transmitted or received data from the internet.  Devices which were
        online, but only transmitted locally are NOT listed.  If there were no
        active devices, this field is omitted.
    """

    device_mac_desc = """
        The mac address of the active device being reported.
    """

    device_tx_desc = """
        This is the total number of bytes sent by the Device to the internet in
        the hour.  Data which was sent locally is not included, only data routed
        out to the public internet is included.
    """

    device_rx_desc = """
        This is the total number of bytes received by the Device from the internet in
        the hour.  Data which was received locally is not included, only data routed
        in from the public internet to the device is included.
    """

    cmd = "data usage"
    name = "DataUsage"
    title = "Data Usage"
    summary = "Advise the Backend of the data usage for the hour."

    devices_fields = f"""
        {{
            {Field.mac("mac", device_mac_desc)},
            {Field.int64("tx", device_tx_desc)},
            {Field.int64("rx", device_rx_desc)}
        }}
    """

    extra_fields = f"""
        {Field.int64("tx", adapter_tx_desc)},
        {Field.int64("rx", adapter_rx_desc)},
        {Field.array("devices", devices_desc, items=
            Field.object(None,devices_desc,["mac","tx","rx"],
                        fields=devices_fields))}
    """

    extra_example = """
        "tx"       : 9876543,
        "rx"       : 1234567,
        "devices"  : [
            {
                "mac" : "54:67:D5:97:97:F0",
                "tx" : 63472,
                "rx" : 23452
            },
            {
                "mac" : "70:9A:63:CA:31:FC",
                "tx" : 82453,
                "rx" : 89783
            }
        ]
    """

    extra_required = '"tstamp", "tx", "rx"'

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


def data_usage_channel():
    """Adapter/Device Data Usage Reporting messages."""
    description = """
        These are messages related to the periodic reporting of data usage.
    """

    subscribe_desc = "Data Usage messages."
    subscribe_msgs = [data_usage()]

    return channel(
        description,
        "Data Usage",
        sub_desc=subscribe_desc,
        sub_msgs=subscribe_msgs,
        tags=[TAGS.ADAPTER_MSGS, TAGS.DEVICE_MSGS],
    )
