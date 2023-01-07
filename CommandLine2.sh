#!/bin/bash

# Initialize an empty array to store the hero names
heroes=()

# Initialize an empty array to store the hero counts
counts=()

# Read each line of the file
while read -r line; do
  # Split the line into the hero and comic fields
  hero=$(echo "$line" | cut -d ',' -f 1)
  comic=$(echo "$line" | cut -d ',' -f 2)

  # Check if the hero is in the list
  found=0
  for i in "${!heroes[@]}"; do
    if [[ "${heroes[$i]}" == "$hero" ]]; then
      # If the hero is in the list, increment the count
      counts[$i]=$((counts[$i] + 1))
      found=1
      break
    fi
  done

  # If the hero was not found in the list, add it and set the count to 1
  if [[ "$found" -eq 0 ]]; then
    heroes+=("$hero")
    counts+=("1")
  fi
done < /Users/simonefacchiano/Desktop/Data_Science/ADM/ADM_HW5/archive-2/edges-small.csv

# Print out the hero names and counts
for i in "${!heroes[@]}"; do
  echo "${heroes[$i]}: ${counts[$i]} comics"
done