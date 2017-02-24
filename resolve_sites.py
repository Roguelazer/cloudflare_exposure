import socket
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=argparse.FileType('r'))
    parser.add_argument('output_base')
    args = parser.parse_args()

    ipv4_output = open(args.output_base + '.resolved_ipv4.txt', 'w')
    ipv6_output = open(args.output_base + '.resolved_ipv6.txt', 'w')

    for line in args.input:
        line = line.strip()
        ip4s = set()
        ip6s = set()
        try:
            for result in socket.getaddrinfo(line, 443):
                if result[0] == socket.AF_INET:
                    ip4s.add(result[-1][0])
                if result[0] == socket.AF_INET6:
                    ip6s.add(result[-1][0])
            for ip in sorted(ip4s):
                ipv4_output.write('{0} {1}\n'.format(ip, line))
            for ip in sorted(ip6s):
                ipv6_output.write('{0} {1}\n'.format(ip, line))
        except socket.gaierror:
            continue


main()
