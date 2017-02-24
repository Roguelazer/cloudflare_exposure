from __future__ import print_function

import argparse
import collections
import radix
import sys
import re


Finding = collections.namedtuple('Finding', ['ip_address', 'domain', 'route_path', 'cloudflare_asns_in_route_path'])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('asn_file', type=argparse.FileType('r'))
    parser.add_argument('route_file', type=argparse.FileType('r'))
    parser.add_argument('resolved_file', type=argparse.FileType('r'))
    args = parser.parse_args()

    rtree = radix.Radix()

    asns = {}
    print('Loading ASNs...', file=sys.stderr)
    for line in args.asn_file:
        rmd = re.match(r'^ ([0-9]+)\s+(\S+)\s+.*', line)
        if rmd:
            asns[int(rmd.group(1))] = rmd.group(2)
    print('...done; loaded {0} ASNs'.format(len(asns)), file=sys.stderr)

    cloudflare_asns = set(k for k, v in asns.items() if 'CLOUDFLARE' in v)

    print('Loading routes into radix tree...', file=sys.stderr)
    for line in args.route_file:
        line = line.strip()
        if line.endswith(' ') or ' ' not in line:
            continue
        prefix, route_path = line.split(' ', 1)
        route_path = tuple(int(i) for i in route_path.split(' '))
        rnode = rtree.add(prefix)
        rnode.data.setdefault("route_paths", set()).add(route_path)
    print('...done', file=sys.stderr)

    bad = []

    print('Processing resolved domains...', file=sys.stderr)
    for line in args.resolved_file:
        line = line.strip()
        address, domain = line.split(' ', 1)
        rnode = rtree.search_best(address)
        if rnode:
            for route_path in rnode.data['route_paths']:
                cloudflare_asns_in_route_path = set(route_path) & cloudflare_asns
                if cloudflare_asns_in_route_path:
                    f = {
                        'address': address,
                        'domain': domain,
                        'route_path': ' '.join(map(str, route_path)),
                        'cloudflare_asns_in_route_path': list(cloudflare_asns_in_route_path),
                    }
                    print(f)
                    bad.append(f)
    print('...done', file=sys.stderr)

main()
