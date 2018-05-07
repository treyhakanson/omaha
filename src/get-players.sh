#! /usr/bin/env bash
BASE_URL="https://www.pro-football-reference.com"
ROOT_DIR="../raw/players"

for link in $( cat ../raw/misc/player-links.txt )
do
   echo "Retrieving $BASE_URL$link"
   fname_raw=$( echo $link | cut -c 2- )
   fname="${fname_raw////.}"
   curl "$BASE_URL$link" > "$ROOT_DIR/$fname"
   echo ""
done
