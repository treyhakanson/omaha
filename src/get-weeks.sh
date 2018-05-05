#! /usr/bin/env bash
BASE_URL="https://www.pro-football-reference.com/years"
ROOT_DIR="../raw/schedules"

for i in {2017..2017} # years
do
   for j in {1..17} # weeks
   do
      echo "Retrieving $BASE_URL/$i/week_$j.htm..."
      curl "$BASE_URL/$i/week_$j.htm" > "$ROOT_DIR/$i.week$j.htm"
      echo ""
   done
done
