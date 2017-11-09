# SNMPv6

Enumerate IPv6 addresses using SNMP

## Dependencies

* pysnmp

`pip install -r requirements.txt`

## Usage

```
usage: snmpv6.py [-h] -i IPADDRESS -c COMMUNITY

Get IPv6 Addresses via SNMP

optional arguments:
  -h, --help    show this help message and exit

required arguments:
  -i IPADDRESS  ip address of the remote host
  -c COMMUNITY  community (public, private, etc.)
```

IP address and community are required.

Example:

`python snmpv6.py -i 192.168.1.10 -c public`
