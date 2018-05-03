#! /usr/bin/env bash
re="([0-9]+),([0-9]+),(/boxscores/(.*).htm)"
BASE_URL="https://www.pro-football-reference.com"

for line in $(cat "./raw/misc/boxscore-links.csv")
do
   if [[ $line =~ $re ]]
   then
      year="${BASH_REMATCH[1]}"
      week="${BASH_REMATCH[2]}"
      link="${BASH_REMATCH[3]}"
      game="${BASH_REMATCH[4]}"
      echo "Retrieving $BASE_URL$link..."
      curl "$BASE_URL$link" > "./raw/boxscores/$year.week$week.$game.htm"
      echo ""
   else
      echo ""
      echo "**An error occurred on file: $link**"
      echo ""
   fi
done
