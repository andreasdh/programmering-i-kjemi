#!/usr/bin/env bash
set -Eeuo pipefail

out="${1:-_build/html/basthon}"
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
backup="$root/vendor/basthon/basthon-console-custom.tgz"
checksum="$backup.sha256"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

valid() {
  [[ -f "$1/index.html" ]] && [[ -d "$1/assets" ]] &&
    find "$1/assets" -maxdepth 1 -type f -name 'main.*.js' ! -name '*.map' -print -quit | grep -q .
}

install_dir() {
  rm -rf "$out"
  mkdir -p "$out"
  cp -a "$1/." "$out/"
}

from_pages() {
  echo "Trying Basthon from origin/gh-pages"
  mkdir -p "$tmp/pages"
  git fetch origin gh-pages --depth=1 || return 1
  git archive --format=tar origin/gh-pages basthon 2>/dev/null |
    tar -xf - -C "$tmp/pages" 2>/dev/null || return 1
  valid "$tmp/pages/basthon" || return 1
  install_dir "$tmp/pages/basthon"
}

from_backup() {
  echo "Trying local Basthon backup"
  [[ -f "$backup" ]] || return 1
  tar -tzf "$backup" >/dev/null || return 1
  mkdir -p "$tmp/backup"
  tar -xzf "$backup" -C "$tmp/backup"
  valid "$tmp/backup" || return 1
  install_dir "$tmp/backup"
}

from_download() {
  echo "Downloading Basthon from the official server"
  archive="$tmp/basthon-console.tgz"
  curl --fail --location --silent --show-error \
    --retry 5 --retry-all-errors --retry-delay 5 \
    --connect-timeout 20 --max-time 240 \
    -o "$archive" https://console.basthon.fr/basthon-console.tgz
  tar -tzf "$archive" >/dev/null
  mkdir -p "$tmp/download"
  tar -xzf "$archive" -C "$tmp/download"
  valid "$tmp/download"
  js=$(find "$tmp/download/assets" -maxdepth 1 -type f -name 'main.*.js' ! -name '*.map' -print -quit)
  python "$root/scripts/customize_basthon.py" "$tmp/download/index.html" "$js"
  install_dir "$tmp/download"
}

mkdir -p "$out"
if from_pages; then
  source_name="gh-pages"
elif from_backup; then
  source_name="local backup"
elif from_download; then
  source_name="official download"
else
  echo "Could not prepare Basthon from any source" >&2
  exit 1
fi

examples=("$root"/docs/_static/basthon_examples/*.py)
[[ -e "${examples[0]}" ]] || { echo "No Basthon examples found" >&2; exit 1; }
rm -rf "$out/examples"
mkdir -p "$out/examples"
cp "${examples[@]}" "$out/examples/"

mkdir -p "$(dirname "$backup")"
candidate="$tmp/basthon-console-custom.tgz"
tar --sort=name --mtime='UTC 2020-01-01' --owner=0 --group=0 --numeric-owner \
  --exclude='./examples' --exclude='./examples/*' -C "$out" -cf - . |
  gzip -n > "$candidate"

size=$(stat -c '%s' "$candidate")
(( size < 95000000 )) || { echo "Basthon backup is too large for GitHub" >&2; exit 1; }
if [[ ! -f "$backup" ]] || ! cmp -s "$candidate" "$backup"; then
  install -m 0644 "$candidate" "$backup"
  echo "Updated local Basthon backup"
fi
(
  cd "$(dirname "$backup")"
  sha256sum "$(basename "$backup")" > "$(basename "$checksum")"
)

echo "Basthon ready from $source_name"
