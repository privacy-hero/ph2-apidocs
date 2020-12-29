"""API Changelog.

List latest changes first.  Order should be descending.
"""
from .xref import Xref


CHANGELOG = f"""
    ## CHANGELOG

    ### V0.1.9

    1. Field name changes to bring consistent with websocket.
         ad-blocking became adblocking
    2. Field name changes in {Xref.streaming_cfg} changed. "ip" -> "ip-proxy",
       "mask" -> "range", "addrs" -> "servers".

    ### V0.1.8

    1. Added VPN Bypass Configuration message: {Xref.vpn_set_bypass_domain}.
    2. And its reply: {Xref.vpn_bypass_domain_reply}.
    3. Added {Xref.vpn_set_bypass_domain} to messages sent in reply to
       {Xref.link_established}.
    4. Renamed fields in {Xref.vpn_set_bypass_domain} to `positive` and `negative`.

    ### V0.1.7

    1. "adultcontent" was renamed to "adult-block" to unify with REST Api.

    ### V0.1.6

    1. Added Local Timezone to {Xref.initial_config} message.
    2. Removed obsolete message data from {Xref.initial_config} message.

    ### V0.1.5

    1. Added {Xref.block_list} message.
    2. Added {Xref.block_list_applied} message.
    3. Referenced blocklist config messages from {Xref.link_established}.
    4. Added all current config messages needed to be sent on startup to
       {Xref.link_established}.

    ### V0.1.4

    1. Broke down the messages into smaller groups to ease document navigation.
    2. Added {Xref.wifi_configuration} message.
    3. Added {Xref.streaming_auth} message.

    ### V0.1.3

    1. Fix Example for {Xref.device_information}
    2. Better document how the speed and latency are calculated in
       {Xref.vpn_server_connect}
    3. Better explain that {Xref.vpn_server_connect} message with an empty list
       of servers is to be used as a vpn_disconnect message.

    ### V0.1.2

    1. Modified speedtest result message {Xref.speedtest_result} to track pperf
       implementation on router.
    2. Changed organization of VPN server configuration in
       {Xref.vpn_server_connect}.
    3. {Xref.vpn_connection_status} updated to track new server id field.

    ### V0.1.1

    1. Added the Adapter Reset {Xref.reset_router} message.
    2. Added the Adapter Resetting {Xref.router_resetting} reply.



    ### V0.1.0

    1. Added hyperlinks between messages to ease navigation.
    2. Added WPS service enable to {Xref.adapter_services} message (and reply
       {Xref.adapter_service_state}).
    3. Added Subscribed service enable to {Xref.adapter_services} message (and
       reply {Xref.adapter_service_state}).
    4. Removed "VPN" from {Xref.adapter_services} (and reply
       {Xref.adapter_service_state}).
    5. Added {Xref.vpn_server_connect} message.
    6. Added {Xref.vpn_server_reconnect} message.
    7. Added {Xref.vpn_connection_status} message.
    8. Made ID field optional but present in every message by including in the
       {Xref.base_msg} specification.
    9. Created {Xref.unsubscribed_whitelist} message to set configuration
       whitelist of domains which are still accessible when the router
       subscription is invalid.
    10. Add list of config messages sent by backend as a result of initial
        connection.
    11. Add the {Xref.wps_status} message.
"""
