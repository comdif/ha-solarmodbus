#!/bin/bash
set -e
D=$(mktemp -d)
curl -fsSL "$1" -o "$D/x.zip"
unzip -o "$D/x.zip" -d "$D"
N=$(ls "$D")

# detect HA config dir
for p in /config ~/.homeassistant /usr/share/hassio/homeassistant; do
    [ -d "$p" ] && CFG="$p" && break
done

# detect custom_components
CC="$CFG/custom_components"
mkdir -p "$CC"

rm -rf "$CC/$N"
cp -r "$D/$N" "$CC/"

# restart HA depending on install type
if command -v ha >/dev/null 2>&1; then
    ha core restart
elif systemctl list-units | grep -q home-assistant; then
    systemctl restart home-assistant
fi
