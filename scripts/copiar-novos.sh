#!/bin/sh

SRC="${1:-/source_dir}"
DST="${2:-/dest_volume_dir}"

echo "Copying new/updated files from $SRC to $DST ..."

cp -ru "$SRC"/. "$DST"/

echo "Copy complete."