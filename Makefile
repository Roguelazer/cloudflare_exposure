.PHONY: safari
safari: asn.txt ip_table.txt ipv6_table.txt userdata/safari_resolved_ipv4.txt userdata/safari_resolved_ipv6.txt venv
	./venv/bin/python lookup.py asn.txt ip_table.txt userdata/safari_resolved_ipv4.txt
	./venv/bin/python lookup.py asn.txt ipv6_table.txt userdata/safari_resolved_ipv6.txt

userdata/safari_resolved_ipv4.txt userdata/safari_resolved_ipv6.txt: userdata/safari_domains.txt
	./venv/bin/python resolve_sites.py $< userdata/safari_resolved_ipv4.txt userdata/safari_resolved_ipv6.txt

userdata/safari_domains.txt: venv
	sqlite3 ~/Library/Safari/History.db 'SELECT url FROM history_items' | grep '^https' | sed -e 's,^https://,,' | cut -d/ -f 1 | sort -u | head -n 10 > $@

venv: requirements.txt
	python3 -m virtualenv venv
	./venv/bin/pip install -r requirements.txt
