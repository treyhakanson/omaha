#!/usr/bin/env bash
BASE_URL="https://www.footballdb.com/transactions/injuries.html"
ROOT_DIR="../raw/injuries"

for i in {2017..2017}
do
   for j in {1..17}
   do
      url="$BASE_URL?yr=$i&wk=$j&type=reg"
      echo "Retrieving injury report for $url..."
      curl "$url" > "$ROOT_DIR/$i.week$j.html"
      echo ""
   done
done
