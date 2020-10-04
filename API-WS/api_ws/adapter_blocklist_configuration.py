"""AsyncAPI Main Defintions.

Privacy Hero 2 - Websocket API - Adapter Configuration Message Definitions.
"""

# from .util import mls
from .schemas import base_message, channel, Field
from .tags import TAGS
from .xref import Xref

# ------------------------------------------------------------------------------


def configure_hostname_blocklists(reply=False):
    """Configure the hostname blocklists."""
    if not reply:
        cmd = "block-list"
        name = "BlockList"
        title = "Block List"
        summary = "Configure URL the Adapter retrieves the blocklists from."

        description = f"""
            This message causes the adapter to update the URL of the known
            hostlists that are blocked for the various categories of blocking we
            employ.  Upon receipt, the router should look up and re-download any
            hostname file specified, even if that name ahs not changed since the
            last receipt of this message.

            Replied to with a {Xref.block_list_applied} message.
        """

        category_desc = """
            A Category of block list URLs being configured.
        """

        tstamp_desc = """
            The request timestamp of the configuration, this tstamp must be returned
            in the reply with the results as the message tstamp.  In the
        """

        blacklist_desc = """
            URLs of blacklists to apply.
        """

        whitelist_desc = """
            URLs of whitelists to apply.
        """

    else:
        cmd = "block-list-applied"
        name = "BlockListApplied"
        title = "Block List Applied"
        summary = (
            "The Acknowledgement that the updated blocklist urls have been applied."
        )

        description = f"""
            This is the reply to setting the block list URL with the
            {Xref.block_list} message.
            \\
            This message is sent after the blocking service has been
            re-configured with the new URL, and triggered to re-download it (if
            necessary).
        """

        category_desc = """
            The category of blocklist that was applied.
        """

        tstamp_desc = """
            The response tstamp, as taken from the original command in the case
            of a reply, OR the tstamp the state changed on the adapter if sent asynchronously.
        """

        blacklist_desc = """
            URLs of blacklists which were applied.
        """

        whitelist_desc = """
            URLs of whitelists which were applied.
        """

    extra_example = """
        "list name" : "safesearch",
        "blacklist" : ["https://our.s3.bucket/safesearch.lst"],
        "whitelist" : []
    """

    extra_fields = f"""
        {Field.enum("list name",category_desc,["adblock","adult","safesearch","youtube"])},
        {Field.array("blacklist", blacklist_desc, Field.url(None, "A blacklist URL"))},
        {Field.array("whitelist", whitelist_desc, Field.url(None, "A whitelist URL"))}
    """

    extra_required = """
        "tstamp", "list name", "blacklist","whitelist"
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


def adapter_blocklist_configuration_channel():
    """Adapter Blocklist Config messages."""
    description = """
        These are messages related to the configuration of the adapter.

        They configure the blocklist URLs where the actual blocklists are
        fetched from.

        These messages are sent on initial connection and also periodically as
        required to reflect user changes in the configuration.
    """

    subscribe_desc = "Configuration Acknowledgements from the Adapter"
    subscribe_msgs = [
        configure_hostname_blocklists(reply=True),
    ]

    publish_desc = "Commands to set the Adapter Configuration."
    publish_msgs = [configure_hostname_blocklists()]

    return channel(
        description,
        "Adapter Blocklist Configuration",
        sub_desc=subscribe_desc,
        sub_msgs=subscribe_msgs,
        pub_desc=publish_desc,
        pub_msgs=publish_msgs,
        tags=TAGS.ADAPTER_MSGS,
    )
