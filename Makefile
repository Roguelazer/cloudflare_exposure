all:
	echo "Read the README"

.PHONY: chrome
chrome: chrome.jsons
	echo "Output is in $<; use jq to manipulate"

.PHONY: safari
safari: safari.jsons
	echo "Output is in $<; use jq to manipulate"

.PHONY: custom
custom: custom.jsons
	echo "Output is in $<; use jq to manipulate"

.PHONY: 1password
1password: 1password.jsons
	echo "Output is in $<; use jq to manipulate"

%.jsons: asn.txt ip_table.txt ipv6_table.txt userdata/%.resolved_ipv4.txt userdata/%.resolved_ipv6.txt venv
	rm -f $@
	./venv/bin/python lookup.py asn.txt ip_table.txt userdata/$(patsubst %.jsons,%,$@).resolved_ipv4.txt >> $@
	./venv/bin/python lookup.py asn.txt ipv6_table.txt userdata/$(patsubst %.jsons,%,$@).resolved_ipv6.txt >> $@

userdata/%.resolved_ipv4.txt userdata/%.resolved_ipv6.txt: userdata/%_domains.txt resolve_sites.py venv
	./venv/bin/python resolve_sites.py $< `echo "$@" | cut -d. -f 1`

userdata/chrome_domains.txt: userdata/Chrome_History.sqlite
	sqlite3 $< 'SELECT url FROM urls' | grep '^https' | sed -e 's,https://,,' | cut -d/ -f 1 | sort -u > $@

userdata/safari_domains.txt:
	sqlite3 ~/Library/Safari/History.db 'SELECT url FROM history_items' | grep '^https' | sed -e 's,^https://,,' | cut -d/ -f 1 | sort -u > $@

userdata/1password_domains.txt: extract_1password_domains.sh
	bash $< | sort -u > "$@"

venv: requirements.txt
	python3 -m virtualenv venv
	./venv/bin/pip install -r requirements.txt

tables: get_routing_table.py venv
	./venv/bin/python get_routing_table.py ip
	./venv/bin/python get_routing_table.py ipv6
