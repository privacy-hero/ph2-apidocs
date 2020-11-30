"""Page Cross references.

Contains page cross references to ease document references.
"""

# TODO: Where possible update the link to the operation link.


class Xref:  # pylint: disable=too-few-public-methods
    """Individual Message Cross References."""

    base_msg = "[*Base Message*](#message-BaseMsg)"
    multi_msg = "[*Multi Message*](#message-MultiMsg)"
    aws_internal_err = "[*AWS Internal Server Error*](#message-AWSInternalServerError)"
    aws_server_error = "[*AWS Server Error*](#message-AWSServerError)"
    initial_config = "[*Initial Configuration*](#message-InitialConfig)"
    unsubscribed_whitelist = (
        "[*Unsubscribed Whitelist*](#message-UnsubscribedWhitelist)"
    )
    link_established = "[*Link Established*](#message-LinkEstablished)"
    adapter_services = "[*Adapter Services*](#message-AdapterServices)"
    adapter_service_state = "[*Adapter Service State*](#message-AdapterServicesState)"
    log_msg = "[*Log Message*](#message-LogMsg)"
    run_speedtest = "[*Run Speedtest*](#message-RunSpeedTest)"
    speedtest_result = "[*Speedtest Result*](#message-SpeedTest)"
    known_devices = "[*Known Devices*](#message-KnownDevices)"
    device_information = "[*Device Information*](#message-DeviceInformation)"
    change_device_state = "[*Change Device State*](#message-ChangeDeviceState)"
    set_bedtime = "[*Set Bedtime*](#message-SetBedtime)"
    delay_bedtime = "[*Delay Bedtime*](#message-DelayBedtime)"
    device_state_changed = "[*Device State Changed*](#message-DeviceStateChanged)"
    bedtime_set = "[*Bedtime Set*](#message-BedtimeSet)"
    bedtime_delayed = "[*Bedtime Delayed*](#message-BedtimeDelayed)"
    data_usage = "[*Data Usage*](#message-DataUsage)"
    vpn_server_connect = "[*VPN Server Connect*](#message-VPNConnect)"
    vpn_server_reconnect = "[*VPN Server Reconnect*](#message-VPNReconnect)"
    vpn_connection_status = "[*VPN Connection Status*](#message-VPNStatus)"
    wifi_configuration = "[*WIFI Configuration*](#message-WifiConfiguration)"
    wps_status = "[*WPS Status*](#message-WPSStatus)"
    streaming_cfg = "[*Streaming Cfg*](#message-ConfigureStreaming)"
    streaming_auth = "[*Streaming Auth*](#message-AuthorizeStreaming)"
    reset_router = "[*Reset Router*](#message-Reset)"
    router_resetting = "[*Router Reseting*](#message-Resetting)"
    block_list = "[*Block List Cfg*](#operation-publish-BLOCKLIST_CFG)"
    block_list_applied = "[*Block List Applied*](#operation-subscribe-BLOCKLIST_CFG)"

    vpn_set_bypass_domain = "[*Set VPN Bypass Domains*](#message-VPNSetBypassDomain)"
    vpn_bypass_domain_reply = (
        "[*Set VPN Bypass Domains Reply*](#message-VPNBypassDomain)"
    )
