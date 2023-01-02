#!/bin/bash

# Make sure the script has the correct permissions to execute
# if [ ! -x /Users/simonefacchiano/scripts/extract_pairs.sh ]; then
#   echo "Error: NO PERMISSIONS"
#   exit 1
# fi

# Initialize an empty array to store the hero pairs
pairs=()

# Initialize an empty array to store the hero pair counts
counts=()

# Read each line of the file
while read -r line; do
  # Split the line into the hero1 and hero2 fields
  hero1=$(echo "$line" | cut -d ',' -f 1)
  hero2=$(echo "$line" | cut -d ',' -f 2)

  # Print the intermediate hero1 and hero2 fields
  #echo "hero1: $hero1"
  #echo "hero2: $hero2"

  # Check if the hero pair is in the list

  found=0
  for i in "${!pairs[@]}"; do
    if [[ "${pairs[$i]}" == "$hero1-$hero2" || "${pairs[$i]}" == "$hero2-$hero1" ]]; then
      # If the hero pair is in the list, increment the count
      counts[$i]=$((counts[$i] + 1))
      found=1
      break
    fi
  done

  # If the hero pair was not found in the list, add it and set the count to 1
  if [[ "$found" -eq 0 ]]; then
    pairs+=("$hero1-$hero2")
    counts+=("1")
  fi
done < /Users/simonefacchiano/Desktop/Data_Science/ADM/ADM_HW5/archive-2/hero-network-small.csv

# Find the index of the highest count
max_index=0
for i in "${!counts[@]}"; do
  if [[ "${counts[$i]}" -gt "${counts[$max_index]}" ]]; then
    max_index=$i
  fi
done

# Print out the most popular hero pair
echo "Most popular hero pair: ${pairs[$max_index]} (${counts[$max_index]} appearances)"
