#!/bin/bash

( 
    for cachedir in ~/Library/Containers/*.agilebits.onepassword-osx-helper/Data/Library/Caches/Metadata/1Password; do
        find "$cachedir" -type f | while read -r fname ; do
            if grep -q "websiteURLs" "$fname" ; then
                jq -r '.websiteURLs| . []' < "$fname"  | tr -d ' '
            fi
        done
    done
) | grep -v '^http://' | sed -E -e 's,^https://,,' -e 's,/.*,,'| grep -v '^http://' | sed -E -e 's,^https://,,' -e 's,/.*,,' | grep -v '^ *$'
