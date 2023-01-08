#!/bin/bash

# Parsing flags
while getopts 'h:e:' flag; do
  case "$flag" in
    h) hero_network="${OPTARG}" ;;
    e) edges="${OPTARG}" ;;
    *) echo "Please specify the path to the hero_network file (-h) and to the edges file (-e)"
      exit 1 ;;
  esac
done

if (( $OPTIND == 1 )); then
   echo "Please specify the path to the hero_network file (-h) and to the edges file (-e)"
   exit 1
fi

echo "Using the hero network file: $hero_network"
echo "Using the edges file: $edges"
######### 1. What is the most popular pair of heroes (often appearing together in the comics)?

echo "1. Finding the most popular pair of heroes."
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
done < $hero_network

# Find the index of the highest count
max_index=0
for i in "${!counts[@]}"; do
  if [[ "${counts[$i]}" -gt "${counts[$max_index]}" ]]; then
    max_index=$i
  fi
done

# Print out the most popular hero pair
echo "Most popular hero pair: ${pairs[$max_index]} (${counts[$max_index]} appearances)"


######### 2. Number of comics per hero.
echo "2. Finding the number of comics per hero."

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
done < $edges

# Print out the hero names and counts
for i in "${!heroes[@]}"; do
  echo "${heroes[$i]}: ${counts[$i]} comics"
done


######### 3. The average number of heroes in comics.

echo "3. Finding the average number of heroes in comics."
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
done < $edges

# Calculate the average number of heroes per comic
average=$(echo "scale=2; $num_heroes / $num_comics" | bc)

# Print the result
echo "Average number of heroes per comic: $average"