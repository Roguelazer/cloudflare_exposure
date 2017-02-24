This is a more sophisticated set of tools to discover sites that were backed by CloudFlare, by using BGP routing
information. It scans your history to find domains you've visited, then finds out if any of those currently route
through CloudFlare. This should be significantly more accurate than looking at who's using CloudFlare for DNS
(since you can use them as a proxy without using their DNS, and vice versa).

It can't currently discover if they routed through CloudFlare at any time in the past, although a large organization
which records logs of BGP state changes could easily extend it to do so.

Example Output
=============
```
{'address': '104.16.87.39', 'domain': 'account.bethesda.net', 'route_path': '13335 13335', 'cloudflare_asns_in_route_path': [13335]}
{'address': '104.16.88.39', 'domain': 'account.bethesda.net', 'route_path': '13335 13335', 'cloudflare_asns_in_route_path': [13335]}
{'address': '104.25.107.107', 'domain': 'aftership.com', 'route_path': '13335 13335', 'cloudflare_asns_in_route_path': [13335]}
{'address': '104.25.108.107', 'domain': 'aftership.com', 'route_path': '13335 13335', 'cloudflare_asns_in_route_path': [13335]}
{'address': '104.16.24.4', 'domain': 'cloud.digitalocean.com', 'route_path': '13335 13335', 'cloudflare_asns_in_route_path': [13335]}
{'address': '104.16.25.4', 'domain': 'cloud.digitalocean.com', 'route_path': '13335 13335', 'cloudflare_asns_in_route_path': [13335]}
{'address': '104.20.4.32', 'domain': 'ello.co', 'route_path': '13335 13335', 'cloudflare_asns_in_route_path': [13335]}
{'address': '104.20.5.32', 'domain': 'ello.co', 'route_path': '13335 13335', 'cloudflare_asns_in_route_path': [13335]}
```

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

Limitations
===========

  1. This only looks at the domains you give it. It won't check any subdomains or try to download HTML and parse it to
      find included assets. This might miss important stuff!
  1. This can only detect services which are still using CloudFlare to front HTTPS traffic; many sites (e.g., Yelp)
      have switched to other CDNs. Must be a great day to work for Fastly.

Components
==========

*`get_routing_table.py`* connects to the Hurricane Electric looking glass and downloads copies of the IPv4 and/or
IPv6 BGP table subsets that contain CloudFlare records. Initially these were full tables that took several hours to
generate, then I remembered that Quagga lets you apply an AS-PATH regexp. Hurray Quagga.

*`resolve_sites.py`* takes a list of domain names and resolves them, writing out files containing all of the IPv4 
and IPv6 addresses used.

*`lookup.py`* combines those, along with the checked-in map of IANA-assigned ASNs, and determines who's routing
through CloudFlare.

License
=======
This tool is available under the ISC license, a copy of which can be found at [LICENSE.txt](LICENSE.txt). There is no
warrantee, etc.
