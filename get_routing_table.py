#!/usr/bin/env python

from __future__ import print_function

import argparse
import re
import telnetlib
import sys

NETWORK_RE = re.compile(r'^\* [ie](\S+)\s')
ROUTE_RE = re.compile(r'((?:[0-9]+ )+[ie])\r$')


def get_table(conn, family, suffix=''):
    timeout = 10
    if suffix:
        b_suffix = (' ' + suffix).encode('utf-8')
    else:
        b_suffix = b''
    command = 'show {0} bgp{1}\n'.format(family, b_suffix).encode('utf-8')
    conn.write(command)
    current_network = None
    current_routes = set()
    while True:
        body = conn.read_until(b' --More-- ', timeout)
        for line in body.decode('utf-8').split('\n'):
            if not line.strip():
                continue
            nmd = NETWORK_RE.match(line)
            if nmd:
                if current_routes:
                    yield (current_network, current_routes)
                    current_routes = set()
                current_network = nmd.group(1)
            rmd = ROUTE_RE.search(line)
            if rmd:
                route = rmd.group(1)
                route = route.split(' ')
                if route[-1] in ('i', 'e'):
                    route = route[:-1]
                if route[0] == '0':
                    route = route[1:]
                route = ' '.join(route)
                current_routes.add(route)
        if b'route-server> ' in body:
            break
        timeout = 1
        conn.write(' ')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--print-stdout', help='Print to stdout in addition to writing to {proto}_table.txt')
    parser.add_argument('asn_file', type=argparse.FileType('r'))
    parser.add_argument('proto', nargs='+', choices=('ip', 'ipv6'))
    args = parser.parse_args()

    asns = {}
    print('Loading ASNs...', file=sys.stderr)
    for line in args.asn_file:
        rmd = re.match(r'^ ([0-9]+)\s+(\S+)\s+.*', line)
        if rmd:
            asns[int(rmd.group(1))] = rmd.group(2)
    print('...done; loaded {0} ASNs'.format(len(asns)), file=sys.stderr)

    cloudflare_asns = set(k for k, v in asns.items() if 'CLOUDFLARE' in v)
    print('Found {0} CloudFlare ASNs'.format(len(cloudflare_asns)))

    conn = telnetlib.Telnet('route-server.he.net')
    conn.read_until(b'route-server> ')
    for proto in set(args.proto):
        with open(b'{0}_table.txt'.format(proto), 'w') as f:
            for asn in cloudflare_asns:
                for prefix, routes in get_table(conn, proto, 'regexp _{0}_'.format(asn)):
                    if args.print_stdout:
                        print(prefix, routes)
                    for route in routes:
                        f.write('{0} {1}\n'.format(prefix, route))
    conn.write('exit')


main()
