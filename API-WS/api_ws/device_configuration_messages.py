"""AsyncAPI Main Defintions.

Privacy Hero 2 - Websocket API - Device Configuration Message Definitions.

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


DEVICE_SERVICES = [
    "vpn",
    "ad-blocking",
    "device-protection",
    "internet-pause",
    "youtube-restricted",
    "safesearch",
    "adultcontent",
]


def device_states(reply=False):
    """Individual Device State Record."""
    services = DEVICE_SERVICES

    if reply:
        intro = "The service/filter on the device which changed state."
        online = """
            - **online** - If the device is online or not. Only an asynchronous
              state change.
        """
        online_note = """
            **online** is only an asynchronous state change.  it is only ever sent as
            a result of the adapter detecting a device coming online or falling offline.
        """
        services.append("online")

        finishes_desc = """
            **OPTIONAL**, and **ONLY INCLUDED** when a timeout is supplied for the
            state, this field in the reply specifies when the timed operation
            will complete.  It is the Unix Epoch Date/Time as seconds since
            midnight 1970 UTC.
        """

        timeout_field = Field.unixepoch("finishes", finishes_desc)
    else:
        intro = "The service/filter on the device which we wish to change the state of."
        online = ""
        online_note = ""

        timeout_desc = """
            **OPTIONAL**, specifies a duration for the state to be set before it
            changes to the opposite state.  It is specified as the number of
            seconds follwing the receipt and processing of this message.  IF
            this message is present, the reply will have the "finishes" field
            set, which is the time NOW + this timeout, NOW is determined by the
            internal clock of the adapter.

            NOTE: Currently this field will ONLY be sent if required for the
            **internet-pause** state.
        """

        timeout_field = Field.unixepoch("timeout", timeout_desc)

    service_desc = f"""
        {intro}
        - **vpn** - The Device will route through the VPN when True (if VPN is enabled)
        - **ad-blocking** - Ad Blocking is Enabled on the device when True.
        - **device-protection** - Device Protection is Enabled on the device when True.
        - **internet-pause** - Internet is paused for the device when True.
        - **youtube-restricted** - Youtube returns restricted search results when True.
        - **safesearch** - Search Engines return "safe" results when True.
        - **adultcontent** - Adult Content is "blocked" when True.
        {online.strip()}

        Note: **internet-pause** also has a timed mode.  The boolean option in this
        message terminates any timed-pause current on the device and sets the state
        accordingly.
        {online_note.strip()}
    """

    state_desc = """
        - **true** - The service/filter is enabled.
        - **false** - The service/filter is disabled.
    """

    fields = f"""
        {{
            {Field.enum("service",service_desc,services)},
            {Field.boolean("state", state_desc)},
            {timeout_field}
        }}
    """

    return f"""
        {Field.object(None, "Service State", ["service","state"], fields)}
    """


def change_device_state():
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

    cmd = "change device state"
    name = "ChangeDeviceState"
    title = "Change Device State"
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
        {Field.string("id", id_desc, minlength=1, maxlength=256)},
        {Field.array("devices", devices_desc, Field.mac(None, mac_desc))},
        {Field.array("states", states_desc, device_states())}
    """

    extra_example = """
        "id"       : "ODU2NDc1ODAtNjhlYy00NGRhLThiYzgtM2U3YjhjZjdiMGU2",
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


def device_state_changed():
    """Device State Changed."""
    description = """
        This message is sent from the Adapter to the Backend and either confirms
        the adapters request to set state, OR advises that the state changed
        asynchronously without being requested by the backend.
    """

    tstamp_desc = """
        IF this is a reply to the backend setting the device state, this must equal the
        tstamp in the original request.
        IF this is an advice that a state changed asynchronously, this is the time the
        adapter changed/detected the state.
    """

    cmd = "device state changed"
    name = "DeviceStateChanged"
    title = "Device State Changed"
    summary = "Advise the Adapter to change the state of the devices."

    id_desc = """
        **Optional**, ID Field.  This field is only set as a reply to a Change Device
        State command, if that command included an ID Field.
    """

    devices_desc = """
        An array of Device MAC addresses the state changes were applied to.  All
        devices listed had the same state change made as listed in this message.
    """

    mac_desc = """
        The Devices MAC address.  Assumed unique per adapter.  Eg. "00:11:22:33:44:55"
        Also accepts "001122334455" or "00-11-22-33-44-55"
    """

    states_desc = """
        The array of services and states that change.  If this is a reply to the
        Change Device State command from the backend, then it lists the same states
        that were requested by the backend.  If asynchronous state changes occur, the
        actual changes that ocurred are listed only.
    """

    extra_fields = f"""
        {Field.uuid("id", id_desc)},
        {Field.array("devices", devices_desc, Field.mac(None, mac_desc))},
        {Field.array("states", states_desc, device_states(reply=True))}
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


def device_configuration_channel():
    """Device Configuration messages."""
    description = """
        These are messages related to the configuration of known devices.
    """

    subscribe_desc = "Device Configuration messages."
    subscribe_msgs = [device_state_changed()]

    publish_desc = "Device Configuration messages."
    publish_msgs = [change_device_state()]

    return channel(
        description,
        "Device Configuration",
        sub_desc=subscribe_desc,
        sub_msgs=subscribe_msgs,
        pub_desc=publish_desc,
        pub_msgs=publish_msgs,
        tags=TAGS.DEVICE_MSGS,
    )
