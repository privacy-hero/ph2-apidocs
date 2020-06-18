Device Data:
 Data: map[string]string{
                "Hostname": update.Hostname,
                "Class":    update.Class,
                "ClientId": update.ClientId,
            },

        "mac":   d.HW.String(),
        "ip":    d.IP.String(),
        "state": Online/Offline
        ip4 address
        ip6 address


Device Command:
    [List of on/off states]
    [List of device macs to apply the state changes to.]
    id - Just returned in the reply, ignored otherwise

    states : VPN, AdBlocking, DeviceProtection, Restrict Youtube, safe search, Internet Paused (On/Off Only)

    States not present are not changed.

Internet Pause timed:
    Pause duration
    id - Just returned in the reply, ignored otherwise
    [List of device macs to pause]

