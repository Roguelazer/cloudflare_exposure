import socket
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=argparse.FileType('r'))
    parser.add_argument('ipv4_output', type=argparse.FileType('a'))
    parser.add_argument('ipv6_output', type=argparse.FileType('a'))
    args = parser.parse_args()

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
                args.ipv4_output.write('{0} {1}\n'.format(ip, line))
            for ip in sorted(ip6s):
                args.ipv6_output.write('{0} {1}\n'.format(ip, line))
        except socket.gaierror:
            continue


main()
