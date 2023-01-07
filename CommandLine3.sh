#!/bin/bash

# Initialize variables to store the total number of comics and the total number of heroes
num_comics=0
num_heroes=0

# Read each line of the file
while read -r line; do
  # Increment the number of heroes by 1
  num_heroes=$((num_heroes + 1))

  # Split the line into the hero and comic fields
  hero=$(echo "$line" | cut -d ',' -f 1)
  comic=$(echo "$line" | cut -d ',' -f 2)

  # Check if the comic has already been counted
  found=0
  for c in "${comics[@]}"; do
    if [[ "$c" == "$comic" ]]; then
      found=1
      break
    fi
  done

  # If the comic has not been counted, add it to the list and increment the number of comics
  if [[ "$found" -eq 0 ]]; then
    comics+=("$comic")
    num_comics=$((num_comics + 1))
  fi
done < /Users/simonefacchiano/Desktop/Data_Science/ADM/ADM_HW5/archive-2/edges-small.csv

# Calculate the average number of heroes per comic
average=$(echo "scale=2; $num_heroes / $num_comics" | bc)

# Print the result
echo "Average number of heroes per comic: $average"