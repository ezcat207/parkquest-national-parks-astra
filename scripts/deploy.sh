#!/bin/sh
set -eu
node build.mjs
node scripts/check.mjs
# Avoid uploading AppleDouble metadata from removable macOS drives.
staging=$(mktemp -d)
trap 'rm -rf "$staging"' EXIT
rsync -a --exclude='._*' --exclude='.DS_Store' site/ "$staging/"
wrangler pages deploy "$staging" --project-name=parkquest-national-parks-astra --branch=main
