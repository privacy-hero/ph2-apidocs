"""API Changelog.

List latest changes first.  Order should be descending.
"""

CHANGELOG = """
    ## CHANGELOG

    ### V0.1.0

    1. Added hyperlinks between messages to ease navigation.
    2. Added WPS service enable to
       [*"adapter-services"*](#message-AdapterServices) message (and
       [reply](#message-AdapterServicesState)).
    3. Added Subscribed service enable to
       [*"adapter-services"*](#message-AdapterServices) message (and
       [reply]([reply]#message-AdapterServicesState)).
    4. Added VPN Server configuration message
       [*"vpn-servers"*](#message-VPNServers)
    5. Made ID field optional but present in every message by including in the
       [*base message*](#message-BaseMsg) specification.
"""
