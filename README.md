# helium-hotspot-cli

Simple command-line interface for common administration tools for hotspots that
expose management APIs. **This was quickly hacked together to provide a mechanism
for automating onboarding/managing hotspots of large numbers of hotspots.**

**PLEASE CONTRIBUTE!**

## Usage

Every command comes with a built in `--help` option, which explains how to use it.

```console
% hotspot-admin --help
usage: hotspot-admin [-h] {discovery,bobcat,sensecap} ...

Admin tools for Helium hotspots

optional arguments:
  -h, --help            show this help message and exit

tool:
  {discovery,bobcat,sensecap}
                        tool to execute (discovery,bobcat,sensecap)
```
### Discover Hotspots on LAN

```console
% hotspot-admin discovery

Found rak      @ 192.168.1.160 (60:81:fa:01:02:75)
Found sensecap @ 192.168.1.161 (a9d9cc9.localnet / e4:4f:01:46:5c:27)
Found bobcat   @ 192.168.1.249 (4ef9bf0.localnet / e4:4f:01:2a:14:39)
```

### Bobcat

```console
% hotspot-admin bobcat --help
usage: hotspot-admin bobcat [-h] [--all ALL] {discover,fastsync,info,name,peers,reboot,reset,resync,status} ip

positional arguments:
  {discover,fastsync,info,name,peers,reboot,reset,resync,status}
                        action to perform
  ip                    IP address for the hotspot

optional arguments:
  -h, --help            show this help message and exit
  --all ALL             execute action against all found on network
```

#### Reboot

```console
% hotspot-admin bobcat reboot 192.168.5.249
```

## Support

There is no support for this tool. Use at your own risk.

#### TODO

* consider replacing argparse with click (for better documentation in --help)
