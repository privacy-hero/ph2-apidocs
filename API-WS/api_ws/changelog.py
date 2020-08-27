"""API Changelog.

List latest changes first.  Order should be descending.
"""
from .xref import Xref

CHANGELOG = f"""
    ## CHANGELOG

    ### V0.1.0wip

    1. Added hyperlinks between messages to ease navigation.
    2. Added WPS service enable to {Xref.adapter_services} message (and reply
       {Xref.adapter_service_state}).
    3. Added Subscribed service enable to {Xref.adapter_services} message (and
       reply {Xref.adapter_service_state}).
    4. Removed "VPN" from {Xref.adapter_services} (and reply
       {Xref.adapter_service_state}).
    5. Added {Xref.vpn_server_connect} message.
    6. Made ID field optional but present in every message by including in the
       [*base message*](#message-BaseMsg) specification.
    7. Created [*unsubscribed-whitelist*](#message-UnsubscribedWhitelist) msg to
       set configuration whitelist of domains which are still accessible when
       the router subscription is invalid.
    8. Add list of config messages sent by backend as a result of initial
       connection.
"""
