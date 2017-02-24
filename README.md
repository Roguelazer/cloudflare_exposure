This is a more sophisticated set of tools to discover sites that were backed by CloudFlare, by using BGP routing
information. It scans your history to find domains you've visited, then finds out if any of those currently route
through CloudFlare.

It can't currently discover if they routed through CloudFlare at any time in the past, although a large organization
which records logs of BGP state changes could easily extend it to do so.

Usage
=====

### Chrome

Find the History file for the user profile you're interested in. This typically looks like `~/Library/Application\ Support/Google/Chrome/Profile\ 1/History` (where `1` may be some other number). Copy that into the `userdata` directory under the filename `Chrome_History.sqlite`. Then run `make chrome`.

    cp ~/Library/Application\ Support/Google/Chrome/Profile\ 1/History userdata/Chome_History.sqlite
    make chrome

### Safari

Safari doesn't have profiles, so this is easy. Run `make safari`

### Checking some custom domains

If you just drop a newline-separated list of domains in `userdata/custom_domains.txt` and run `make custom`, the tool will scan them
for you.

Components
==========

*`get_routing_table.py`* connects to the Hurricane Electric looking glass and downloads copies of the IPv4 and/or
IPv6 full Internet BGP tables. They're also checked-in, because downloading them takes several hours.

*`resolve_sites.py`* takes a list of domain names and resolves them, writing out files containing all of the IPv4 
and IPv6 addresses used.

*`lookup.py`* combines those, along with the checked-in map of IANA-assigned ASNs, and determines who's routing
through CloudFlare.
