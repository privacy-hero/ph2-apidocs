"""AsyncAPI Main Defintions.

Privacy Hero 2 - Websocket API - Adapter VPN Config Message Definitions.
"""

# from .util import mls
from .schemas import base_message, channel, Field
from .tags import TAGS

# ------------------------------------------------------------------------------


def wifi_radio_config(default: bool = False):
    """Individual Wifi Radio Configuration."""
    cfg_fields = f"""
    {{
        {Field.boolean("enabled", "Is the WIFI Enabled or Not.")},
    """
    if not default:
        cfg_fields += f"""
            {Field.enum("band", "The Frequency band the Radio operates in.", ["2.4Ghz","5Ghz","6Ghz"])},
        """

    cfg_fields += f"""
        {Field.string("ssid", "The name of the wifi network.", default="PrivacyHero")},
        {Field.string("key", "The network password (if defined)")},
        {Field.int16("channel", "The preferred channel.  Default to Auto, if not present or set to -1.")},
        {Field.int16("bandwidth", "The preferred channel bandwidth.  Default to Max, if not present or set to -1.")}
    }}
    """

    return cfg_fields


# ------------------------------------------------------------------------------


def wifi_configure():
    """Configure the VPN Servers the Router will communicate with."""
    cmd = "wifi-cfg"
    name = "WifiConfiguration"
    title = "WIFI Configuration"
    summary = "Set up the WIFI Radios following this configuration."

    description = """
        This message causes the router to enable or disable its wifi radios, and
        if enabled, configure them accordingly.
        \\
        * *default* configuration specifies the wifi configuration for all
        radios within the router.  Each individual radio within the router may
        be further configured to differ from the default by the "custom" array.
        * *custom* array.  This array specifies the configuration differences
        requested for each radio within the device.  Any radio which is not
        specified by the array obtains the default configuration.  The only
        mandatory fields are **enabled** and **band**.  If a configuration
        exists for a radio that does not exist, it is silently ignored.  The
        array is optional, and may not be sent in the message if there are no
        per-radio customizations to apply.
        \\
        * *channel* setting defines the numeric channel preference for the
        radio.  If the field is missing, or set to -1, then the channel is to be
        auto selected by the router.  If the **channel** is set, the router will
        set the actual channel to the closest valid numeric channel  for the
        radio.  IF the router is unable to determine which channel is being
        requested, it simply defaults to AUTO, and does not reject the message.
        * *bandwidth* setting defines the radio channel bandwidth.  If the
        setting is missing, or is set to -1, the bandwidth defaults to the
        widest available channel bandwidth for the radio.  This is because
        devices should be able to downgrade their individual connection based on
        their capabilities and interference, and the widest channel allows for
        the greatest speed.  If the bandwidth is specified, the router sets the
        bandwidth to the closest numerical bandwidth valid for the particular
        radio.  For example,  a bandwidth setting of 75 would select 80Mhz
        bandwidth, and not 40Mhz.
        \\
        *NOTE:*  Both *channel* and *bandwidth* are preferences and not hard
        configuration.  The router is to attempt to make a best effort attempt
        to follow the preference and if it can not, default to a reasonable
        value, or auto select as the case dictates.  Neither fields should cause
        the configuration to be rejected, and if the router is unable to change
        either setting, it will still accept the message if they are defined.
    """

    tstamp_desc = """
        The request timestamp of the configuration.
    """

    extra_example = """
        "default": {
            "enabled" : true,
            "ssid" : "MyHouse",
            "key"  : "its a secret"
        }
    """

    extra_fields = f"""
        {Field.object("default","Default Wifi Configuration for all radios",
                      required=["enabled"], fields=wifi_radio_config(default=True))},
        {Field.array("custom", "A list of customizations to apply per radio.",
                      Field.object(None,"Custom Wifi Channel Configuration",
                      required=["enabled","band"], fields=wifi_radio_config()))}
    """

    extra_required = """
        "tstamp", "default"
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


def wifi_configuration_channel():
    """Adapter WIFI Config messages."""
    description = """
        These are messages related to the configuration of the WIFI Radios in the adapter.
        \\
        These messages are sent on initial connection and also periodically as
        required to reflect user changes in the configuration.
    """

    subscribe_desc = None
    subscribe_msgs = None

    publish_desc = "Messages to set the Adapter Wifi Configuration."
    publish_msgs = [wifi_configure()]

    return channel(
        description,
        "Adapter WIFI Configuration",
        sub_desc=subscribe_desc,
        sub_msgs=subscribe_msgs,
        pub_desc=publish_desc,
        pub_msgs=publish_msgs,
        tags=TAGS.ADAPTER_MSGS,
    )
