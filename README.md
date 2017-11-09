# SNMPv6

Enumerate IPv6 addresses using SNMP

## Dependencies

* pysnmp

`pip install -r requirements.txt`

## Usage

```
usage: snmpv6.py [--help] -h HOST -c COMMUNITY

Get IPv6 Addresses via SNMP

optional arguments:
  --help

required arguments:
  -h HOST       ip address of the remote host
  -c COMMUNITY  community (public, private, etc.)
```

Host and Community are required.

Examples:

`python snmpv6.py -h demo.snmplabs.com -c public`
`python snmpv6.py -h 104.236.166.95 -c private`
