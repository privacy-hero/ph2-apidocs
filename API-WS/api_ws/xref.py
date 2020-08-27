"""Page Cross references.

Contains page cross references to ease document references.
"""


class Xref:  # pylint: disable=too-few-public-methods
    """Individual Message Cross References."""

    base_msg = "[*Base Message*](#message-BaseMsg)"
    multi_msg = "[*Multi Message*](#message-MultiMsg)"
    aws_internal_err = "[*AWS Internal Server Error*](#message-AWSInternalServerError)"
    aws_server_error = "[*AWS Server Error*](#message-AWSServerError)"
    initial_config = "[*Initial Configuration*](#message-InitialConfig)"
    unsubscribed_whitelist = "[*Unsubscribed Whitlist*](#message-UnsubscribedWhitelist)"
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

    # --------- Undefined links

    get_account_portal = "[*Get Account Portal*]()"
    account_portal = "[*Account Portal*]()"
    vpn_connection_status = "[*VPN Connection Status*]()"
    wps_status = "[*WPS Status*]()"
