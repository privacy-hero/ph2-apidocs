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
from .xref import Xref

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
    description = f"""
        This message is sent from the Backend to the adapter and instructs the adapter
        to make the listed state changes to the listed devices.  The message can
        contain multiple state changes, and multiple devices.  The devices listed are
        all triggered with the same state changes.  The router will reply with a
        {Xref.device_state_changed} reply.
    """

    tstamp_desc = """
        The time the backend decided the state should change.  To be returned in the
        paired reply.
    """

    cmd = "change device state"
    name = "ChangeDeviceState"
    title = "Change Device State"
    summary = "Advise the Adapter to change the state of the devices."

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
        {Field.array("devices", devices_desc, Field.mac(None, mac_desc))},
        {Field.array("states", states_desc, device_states())}
    """

    extra_example = """
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
    description = f"""
        This message is sent from the Adapter to the Backend and either confirms
        the adapters request to set state from the {Xref.change_device_state}
        message, OR advises that the state changed asynchronously without being
        requested by the backend.
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
        {Field.array("devices", devices_desc, Field.mac(None, mac_desc))},
        {Field.array("states", states_desc, device_states(reply=True))}
    """

    extra_example = """
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


def bedtime_schedule(reply=False):  # pylint: disable=unused-argument
    """Individual Bedtime schedule record."""
    start_desc = """
        This is the time bedtime starts on the specificed day.

        This time is minutes since midnight of the specified day.

        IF bedtime starts after the subsequent midnight of the specified day,
        then this time will be greater than 1,440.

        Assuming the specified day is Monday. Example Start Times:
         * 600 = 10am Monday Morning.
         * 1,260 = 9pm Monday Night.
         * 1,350 = 10:30pm Monday Night.
         * 1,530 = 1:30am Tuesday Morning.
    """

    end_desc = """
        This is the time bedtime ends on the specificed day.

        This time is minutes since midnight of the specified day.

        Bedtime typically always ends after the subsequent midnight of the
        specified day, so typically this time will be greater than 1,440.

        start is always < end.  If it is not the schedule is in error and should
        be rejected.

        Assuming the specified day is Monday. Example End Times:
         * 1,800 = 6am Tuesday Morning.
    """

    fields = f"""
        {{
            {Field.daytime("start",start_desc)},
            {Field.daytime("end", end_desc)}
        }}
    """

    return f"""
        {Field.object(None, "Bedtime Schedule", ["start","end"], fields)}
    """


def set_device_bedtime(reply=False):
    """Set Device Bedtime."""
    if not reply:
        cmd = "set bedtime"
        name = "SetBedtime"
        title = "Set Device Bedtime"
        summary = (
            "Advise the Adapter to set the bedtime schedule for the listed devices."
        )

        description = f"""
            This message is sent from the Backend to the adapter and instructs
            the adapter to set the listed bedtime schedule for the listed
            devices.  The devices listed are all set to the same bedtime
            schedule.  The Adapter will receive multiple "set bedtime" messages
            to set the schedules of all known devices.  If the Adapter knows a
            device, but has not received a bedtime schedule for it, it must
            assume there is no bedtime schedule that applies to it.  The full
            set of bedtime schedules are sent during initial configuration, in
            response to the backend receiving the {Xref.link_established}
            message. It is also sent as required to reflect configuration changes
            as they occur.  Once set, the backend replies with the
            {Xref.bedtime_set} message, with the tstamp and id (if present)
            matching those same fields in this request.
        """

        tstamp_desc = """
            The time the backend decided to set the bedtime schedule.  To be returned in the
            paired reply.
        """

        devices_desc = """
            An array of Device MAC addresses the bedtime schedule applies to. All
            devices listed are to have the same bedtime schedule applied to
            them.  Only after all listed devices have the bedtime schedule
            applied does the adapter send the paired reply.
        """
    else:
        cmd = "bedtime set"
        name = "BedtimeSet"
        title = "Device Bedtime Set"
        summary = "Advise the Backend that the bedtime schedule has been set."

        description = """
            This message is sent from the Adapter to the Backend to acknowledge
            that the listed devices bedtime schedule was set as required.
        """

        tstamp_desc = """
            The tstamp, as received in the message which triggered this reply to
            be sent.
        """

        devices_desc = """
            An array of Device MAC addresses the bedtime schedule applied to. All
            devices listed had the same bedtime schedule applied to
            them.  The list must have the same number of devices and same
            device mac addresses as the original request to set the schedule.
        """

    id_desc = """
        ID Field.  The Adapter does not do any processing or verification
        of the ID field, it must be returned verbatim in the paired reply.
    """

    mac_desc = """
        The Devices MAC address.  Assumed unique per adapter.  Eg. "00:11:22:33:44:55"
        Also accepts "001122334455" or "00-11-22-33-44-55"
    """

    schedule_desc = """
        This is an array for a rotating weeks worth of bedtime schedules.
        The first element is Monday, the second Tuesday, Wednesday and so on
        till Sunday.  There will ALWAYS be 7 days present if a schedule is set.

        IF no schedule is to be set for the specified devices, the schedule
        field will be present, and will be set to null.  This means that no
        schedule is to apply to the listed devices.

        IF any single day does not have a bed time, but other days do, then both
        the "start" and "end" will be set to 0 (zero).
    """

    extra_fields = f"""
        {Field.string("id", id_desc, minlength=1, maxlength=256)},
        {Field.array("devices", devices_desc, Field.mac(None, mac_desc))},
        {Field.array("schedule", schedule_desc, bedtime_schedule(reply), 7, 7)}
    """

    extra_example = """
        "id"       : "ODU2NDc1ODAtNjhlYy00NGRhLThiYzgtM2U3YjhjZjdiMGU2",
        "devices" : ["53:CB:12:79:E5:F6","DD:0F:91:FE:9E:00","54:A4:33:F5:D8:A4"],
        "schedule" : [
            {"start" : 1260, "end" : 1800},
            {"start" : 1260, "end" : 1800},
            {"start" : 1260, "end" : 1800},
            {"start" : 1260, "end" : 1800},
            {"start" : 1350, "end" : 1800},
            {"start" : 1350, "end" : 1800},
            {"start" : 1260, "end" : 1800}
        ]
    """

    extra_required = '"tstamp", "id", "devices", "schedule"'

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


def set_device_bedtime_delay(reply=False):
    """Delay Bedtime."""
    if not reply:
        cmd = "delay bedtime"
        name = "DelayBedtime"
        title = "Delay Bedtime"
        summary = "Advise the Router to delay the current or next bedtime start."
        description = f"""
            This message causes the adapter to delay the bedtime for the listed
            devices by the specified number of minutes.  It is a one-shot delay
            and once expired is not repeated.

            IF bedtime has not yet commenced for the day, the delay applies to
            the bedtime which is next to occur.  The delay then causes the start
            to delay by the specified number of minutes.

            IF the bedtime has started but not yet finished, the delay applies
            to the currently active bedtime, and will delay it from its start
            time by the specified number of minutes.  So, for example, if
            started at 10pm and at 10:15pm a delay of 45 minutes was received,
            the devices internet would unpause and would re-pause at 10:45.
            This message is responded to with the {Xref.bedtime_delayed} message
            from the router.
        """

        devices_desc = """
            An array of Device MAC addresses the bedtime delay applies to. All
            devices listed are to have the same bedtime delay applied to
            them.  Only after all listed devices have the bedtime delay
            applied does the adapter send the paired reply.
        """

        delay_desc = """
            The number of minutes we are to delay bedtime for the listed devices
            for.  A delay of zero terminates any currently running delay.  Delay
            time is absolute, from the start of the next/current bedtime.  A
            subsequent delay is NOT an additional delay, it replaces the current delay.
        """
    else:
        cmd = "bedtime delayed"
        name = "BedtimeDelayed"
        title = "Bedtime Delayed"
        summary = (
            "Advise the Adapter that Bedtime has been Delayed for the listed devices."
        )

        description = f"""
            This message advises that a bedtime delay has been applied to the
            devices, and the absolute UTC time when the delay will complete.  It
            is sent in response to a {Xref.set_bedtime} message from the backend.
        """

        devices_desc = """
            An array of Device MAC addresses the bedtime delay applies to. All
            devices listed have had the same bedtime delay applied to
            them.  Only after all listed devices have the bedtime delay
            applied does the adapter send the paired reply.
        """

        delay_desc = """
            The number of minutes we are to delay bedtime for the listed devices
            for.  A delay of zero terminates any currently running delay.  Delay
            time is absolute, from the start of the next/current bedtime.  A
            subsequent delay is NOT an additional delay, it replaces the current delay.
        """

        delay_end_desc = """
            This is the absolute unix epoch time when the delay will finish on
            the adapter for the listed devices.
        """

    tstamp_desc = """
        The time the backend decided to set the bedtime delay.  To be returned in the
        paired reply.
    """

    mac_desc = """
        The Devices MAC address.  Assumed unique per adapter.  Eg. "00:11:22:33:44:55"
        Also accepts "001122334455" or "00-11-22-33-44-55"
    """

    extra_fields = f"""
        {Field.array("devices", devices_desc, Field.mac(None, mac_desc))},
        {Field.daytime("delay", delay_desc)}
    """

    extra_example = """
        "devices" : ["53:CB:12:79:E5:F6","DD:0F:91:FE:9E:00","54:A4:33:F5:D8:A4"],
        "pause" : 45
    """

    extra_required = '"tstamp", "id", "devices", "delay"'

    if reply:
        extra_fields += f"""
        ,
        {Field.unixepoch("ends", delay_end_desc)}
        """

        extra_example += """
            , "ends":  1594391720
        """

        extra_required += ',"ends"'

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
    subscribe_msgs = [
        device_state_changed(),
        set_device_bedtime(reply=True),
        set_device_bedtime_delay(reply=True),
    ]

    publish_desc = "Device Configuration messages."
    publish_msgs = [
        change_device_state(),
        set_device_bedtime(),
        set_device_bedtime_delay(),
    ]

    return channel(
        description,
        "Device Configuration",
        sub_desc=subscribe_desc,
        sub_msgs=subscribe_msgs,
        pub_desc=publish_desc,
        pub_msgs=publish_msgs,
        tags=TAGS.DEVICE_MSGS,
    )
