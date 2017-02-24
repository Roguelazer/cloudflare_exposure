This is a more sophisticated set of tools to discover sites that were backed by CloudFlare, by using BGP routing
information. It scans your history to find domains you've visited, then finds out if any of those currently route
through CloudFlare. This should be significantly more accurate than looking at who's using CloudFlare for DNS
(since you can use them as a proxy without using their DNS, and vice versa).

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

### 1Password

If you use 1Password and have third-party integration, you can run `make 1password` to show which of your saved
1Password logins is affected.

### Checking some custom domains

If you just drop a newline-separated list of domains in `userdata/custom_domains.txt` and run `make custom`, the tool will scan them
for you.

Components
==========

*`get_routing_table.py`* connects to the Hurricane Electric looking glass and downloads copies of the IPv4 and/or
IPv6 BGP table subsets that contain CloudFlare records. Initially these were full tables that took several hours to
generate, then I remembered that Quagga lets you apply an AS-PATH regexp. Hurray Quagga.

*`resolve_sites.py`* takes a list of domain names and resolves them, writing out files containing all of the IPv4 
and IPv6 addresses used.

*`lookup.py`* combines those, along with the checked-in map of IANA-assigned ASNs, and determines who's routing
through CloudFlare.
