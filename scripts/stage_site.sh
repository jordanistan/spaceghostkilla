#!/usr/bin/env bash
set -euo pipefail

# Publish only site files. Internal docs, scripts, and repository configuration
# never enter the Pages artifact.
site_dir="${1:-_site}"
mkdir -p "$site_dir"
shopt -s nullglob
for file in *.html *.css *.js *.xml *.txt *.webmanifest CNAME; do
  [[ -f "$file" ]] && cp "$file" "$site_dir/"
done
for directory in assets .well-known; do
  if [[ -d "$directory" ]]; then
    cp -R "$directory" "$site_dir/"
  fi
done
test -f "$site_dir/index.html"
test -f "$site_dir/CNAME"
